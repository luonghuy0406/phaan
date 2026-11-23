// Coordinates. "world" = desk space (camera-independent). "local" = inside a paper, before its rotation.
// A paper is drawn at translate(x, y) rotate(r × 90°) with the rotation around its centre (CSS default).

export interface Box { x: number; y: number; w: number; h: number; r: number }
export interface Pt { x: number; y: number }
export interface Rect { x: number; y: number; w: number; h: number }

// Quarter-turn rotation in screen space (y down): r = 1 is 90° clockwise, like CSS rotate(90deg).
export function rot(dx: number, dy: number, r: number): [number, number] {
  switch (((r % 4) + 4) % 4) {
    case 1: return [-dy, dx];
    case 2: return [-dx, -dy];
    case 3: return [dy, -dx];
    default: return [dx, dy];
  }
}

export function localToWorld(lx: number, ly: number, b: Box): Pt {
  const [rx, ry] = rot(lx - b.w / 2, ly - b.h / 2, b.r);
  return { x: b.x + b.w / 2 + rx, y: b.y + b.h / 2 + ry };
}

export function worldToLocal(wx: number, wy: number, b: Box): Pt {
  const [rx, ry] = rot(wx - (b.x + b.w / 2), wy - (b.y + b.h / 2), 4 - (b.r % 4));
  return { x: rx + b.w / 2, y: ry + b.h / 2 };
}

// Axis-aligned bounds of a (possibly quarter-turned) box.
export function boundsOf(b: Box): Rect {
  const turned = b.r % 2 === 1;
  const w = turned ? b.h : b.w;
  const h = turned ? b.w : b.h;
  return { x: b.x + (b.w - w) / 2, y: b.y + (b.h - h) / 2, w, h };
}

export function union(rects: Rect[]): Rect | null {
  if (!rects.length) return null;
  const x = Math.min(...rects.map((r) => r.x));
  const y = Math.min(...rects.map((r) => r.y));
  return { x, y, w: Math.max(...rects.map((r) => r.x + r.w)) - x, h: Math.max(...rects.map((r) => r.y + r.h)) - y };
}

export const clamp = (v: number, a: number, b: number) => Math.min(b, Math.max(a, v));

// Shortest distance from p to segment ab.
export function segDist(px: number, py: number, ax: number, ay: number, bx: number, by: number): number {
  const vx = bx - ax;
  const vy = by - ay;
  const len = vx * vx + vy * vy;
  const t = len ? clamp(((px - ax) * vx + (py - ay) * vy) / len, 0, 1) : 0;
  return Math.hypot(px - (ax + t * vx), py - (ay + t * vy));
}
