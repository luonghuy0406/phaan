#!/usr/bin/env python3
"""Tạo bản Supertonic 3 tối ưu cho trình duyệt từ bản fp32 chính thức (Supertone/supertonic-3, OpenRAIL-M).

    python3 -m venv ~/.venvs/onnx && ~/.venvs/onnx/bin/pip install onnx onnxruntime onnxconverter-common
    ~/.venvs/onnx/bin/python tools/optimize-supertonic.py ~/.cache/supertonic3 out/

Kết quả (đặt lên một máy chủ có CORS, rồi trỏ VITE_TTS_MODEL_OPT_BASE tới thư mục chứa fp16/ và int8/):
  out/fp16/onnx/*.onnx  ~200 MB  toàn bộ fp16 (giữ vào/ra fp32) cho WebGPU có shader-f16.
                                 Độ lệch phổ so với fp32 0,7 dB; tốc độ như fp32 trên GPU, tải về bằng một nửa.
  out/int8/onnx/*.onnx  ~186 MB  vector_estimator + text_encoder lượng tử int8 động (MatMul/Gemm/Conv),
                                 vocoder + duration_predictor giữ fp32 (lượng tử vocoder làm hỏng âm thanh).
                                 Cho WebAssembly trên CPU: nhanh hơn fp32 khoảng 25% (4 luồng) đến 2 lần (onnxruntime-node).
Kiểm tra: cả hai bản được chép lại (nhận dạng giọng nói) giống hệt bản fp32 ở 6 bước khử nhiễu.
Sau khi tạo lại, cập nhật kích thước file trong OPT_BYTES (src/lib/supertonic/core.ts).
"""
import os
import shutil
import sys

import onnx
from onnx import TensorProto
from onnxconverter_common import float16
from onnxruntime.quantization import QuantType, quantize_dynamic

NAMES = ['duration_predictor', 'text_encoder', 'vector_estimator', 'vocoder']
INT8 = {'text_encoder', 'vector_estimator'}


def fp16(src: str, dst: str) -> None:
    m = onnx.load(src)
    m.graph.ClearField('value_info')  # stale fp32 annotations would clash with the converted graph
    m = float16.convert_float_to_float16(m, keep_io_types=True, disable_shape_infer=True)
    # attention scales are computed as Cast(to=float) of a shape: make them half too (graph outputs stay fp32)
    outputs = {o.name for o in m.graph.output}
    for node in m.graph.node:
        if node.op_type == 'Cast' and not any(o in outputs for o in node.output):
            for a in node.attribute:
                if a.name == 'to' and a.i == TensorProto.FLOAT:
                    a.i = TensorProto.FLOAT16
    onnx.save(m, dst)


def main(src_dir: str, out_dir: str) -> None:
    for v in ('fp16', 'int8'):
        os.makedirs(f'{out_dir}/{v}/onnx', exist_ok=True)
    for n in NAMES:
        src = f'{src_dir}/onnx/{n}.onnx'
        fp16(src, f'{out_dir}/fp16/onnx/{n}.onnx')
        if n in INT8:
            quantize_dynamic(src, f'{out_dir}/int8/onnx/{n}.onnx', op_types_to_quantize=['MatMul', 'Gemm', 'Conv'], weight_type=QuantType.QUInt8)
        else:
            shutil.copy(src, f'{out_dir}/int8/onnx/{n}.onnx')
        print(n, {v: os.path.getsize(f'{out_dir}/{v}/onnx/{n}.onnx') for v in ('fp16', 'int8')}, flush=True)
    shutil.copy(f'{src_dir}/LICENSE', f'{out_dir}/LICENSE') if os.path.exists(f'{src_dir}/LICENSE') else None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(os.path.expanduser(sys.argv[1]), sys.argv[2])
