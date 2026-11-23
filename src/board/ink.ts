// Handwriting with perfect-freehand: pressure-sensitive with Apple Pencil, simulated pressure for mouse / finger.
import { getStroke } from 'perfect-freehand';
import { segDist } from './geometry';

// A stroke is stored on the surface it was started on, in that surface's local coordinates,
// so it moves and rotates together with the paper / sticky note.
//   t: "world" | "doc:<id>" | "note:<id>"     pts: flat [x, y, pressure, x, y, pressure, …]
export interface Stroke {
  id: string;
  t: string;
  pts: number[];
  c: string;     // colour
  s: number;     // size in world units
  m?: 1;         // marker (highlighter)
  p?: 1;         // real pressure (Apple Pencil)
}

export const PEN_COLORS = [
  { id: 'red', label: 'Đỏ', v: '#c0261b' },
  { id: 'blue', label: 'Xanh', v: '#1f4fa8' },
  { id: 'black', label: 'Đen', v: '#1d1a16' },
];
export const MARKER_COLORS = [
  { id: 'yellow', label: 'Vàng', v: '#f5d22e' },
  { id: 'green', label: 'Xanh lá', v: '#6fdc7a' },
  { id: 'pink', label: 'Hồng', v: '#ff8fb8' },
];
export const PEN_SIZES = [2.2, 3.6, 6];
export const MARKER_SIZES = [14, 22, 32];

const average = (a: number, b: number) => (a + b) / 2;

function svgPath(points: number[][]): string {
  const n = points.length;
  if (n < 4) return '';
  let a = points[0];
  let b = points[1];
  let d = `M${a[0].toFixed(1)},${a[1].toFixed(1)} Q${b[0].toFixed(1)},${b[1].toFixed(1)} ${average(b[0], points[2 % n][0]).toFixed(1)},${average(b[1], points[2 % n][1]).toFixed(1)} T`;
  for (let i = 2; i < n - 1; i++) {
    a = points[i];
    b = points[i + 1];
    d += `${average(a[0], b[0]).toFixed(1)},${average(a[1], b[1]).toFixed(1)} `;
  }
  return `${d}Z`;
}

export function strokePath(st: Pick<Stroke, 'pts' | 's' | 'm' | 'p'>, last = true): string {
  const input: number[][] = [];
  for (let i = 0; i < st.pts.length; i += 3) input.push([st.pts[i], st.pts[i + 1], st.pts[i + 2]]);
  if (input.length === 1) input.push([input[0][0] + 0.1, input[0][1] + 0.1, input[0][2]]);
  const outline = getStroke(input, st.m
    ? { size: st.s, thinning: 0, smoothing: 0.6, streamline: 0.55, simulatePressure: false, last }
    : { size: st.s, thinning: st.p ? 0.62 : 0.5, smoothing: 0.55, streamline: 0.42, simulatePressure: !st.p, last });
  return svgPath(outline);
}

// Does the point (x, y) — in the stroke's own coordinates — touch the stroke?
export function hitStroke(st: Stroke, x: number, y: number, radius: number): boolean {
  const tol = radius + st.s / 2;
  const p = st.pts;
  if (p.length < 6) return Math.hypot(p[0] - x, p[1] - y) <= tol;
  for (let i = 0; i + 5 < p.length; i += 3) {
    if (segDist(x, y, p[i], p[i + 1], p[i + 3], p[i + 4]) <= tol) return true;
  }
  return false;
}

export const strokeLength = (pts: number[]) => {
  let len = 0;
  for (let i = 3; i < pts.length; i += 3) len += Math.hypot(pts[i] - pts[i - 3], pts[i + 1] - pts[i - 2]);
  return len;
};
