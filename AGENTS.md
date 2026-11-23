# Hướng dẫn cho AI agent (Antigravity, Claude, Codex…)

Dự án: website game phá án trên trình duyệt (tối ưu cho iPad + Apple Pencil), gồm nhiều "hồ sơ" (vụ án) chơi trên một bàn điều tra chung.
Stack: Vite + React 18 + TypeScript, `@use-gesture/react` (kéo / chụm), `perfect-freehand` (nét bút), `zustand` + `idb-keyval` (lưu tiến trình vào IndexedDB).

## Lệnh
- `npm install`, rồi `npm run dev` → http://localhost:5173 (thêm `--host` sẵn để mở từ iPad cùng mạng Wi-Fi)
- `npm run validate`: kiểm định mọi hồ sơ. **Chạy sau mọi thay đổi hồ sơ.**
- `npm run sync-cases`: nạp đáp án lên Supabase cho chế độ chơi nhóm. **Chạy sau khi sửa câu hỏi.**
- `npm test`: unit test. `npm run build`: bản production vào `dist/`.

## Cấu trúc
- `src/pages/`: trang chủ (`/`), chi tiết hồ sơ (`/ho-so/:id`), bàn điều tra (`/choi/:id`).
- `src/board/`: engine bàn điều tra. **Không sửa engine khi chỉ đang viết vụ án mới.**
- `public/cases/index.json`: danh mục hồ sơ. `public/cases/<id>/case.json` + `images/`: nội dung một vụ án.
- `authoring/<id>/`: kịch bản gốc và prompt ảnh (chứa lời giải; nằm ngoài `public/` nên không lên web).
- `docs/case-schema.md`: đặc tả `case.json` và nhịp vòng khuyến nghị. **Đọc trước khi viết hồ sơ.**
- `prompts/antigravity/`: quy trình từng bước để tạo một vụ án mới.
- `src/multiplayer/`, `supabase/migrations/`: chơi nhóm. Không bao giờ đưa `SUPABASE_SECRET_KEY` vào code trong `src/` hay biến `VITE_`.

## Quy tắc nội dung
1. Mọi vụ án, nhân vật, địa danh cụ thể (tên quán, tên cơ quan, số nhà) đều hư cấu. Không dùng tên người thật, thương hiệu thật, vụ án có thật.
2. Không sao chép cốt truyện, nhân vật, hình ảnh hay văn bản của game, sách, phim đã có (kể cả các boardgame phá án khác). Được học cấu trúc và nhịp chơi, không được chép nội dung.
3. Viết tiếng Việt chuẩn, có dấu đầy đủ. Văn phong đúng loại giấy tờ (biên bản khô khan, lời khai là văn nói, thư tay có cảm xúc).
4. Công bằng với người chơi: mọi kết luận phải suy ra được từ tài liệu đang mở ở vòng đó.
5. Bạo lực chỉ ở mức gợi tả: không mô tả máu me chi tiết, không ảnh thi thể rõ mặt.
6. Không dùng thẻ HTML trong `case.json`. Chỉ dùng `**đậm**`, `__gạch chân__`, `~~gạch xoá~~`.
7. Ảnh không chứa chữ (chữ do trang web hiển thị), trừ ảnh `scan` là bản chụp tài liệu đã dàn trang. Ảnh lưu `.webp` trong `public/cases/<id>/images/`.
8. Đổi cấu trúc một hồ sơ đã phát hành (thêm, bớt, đánh số lại tài liệu, đổi đáp án) sẽ làm người chơi bắt đầu lại hồ sơ đó. Chỉ làm khi cần.
