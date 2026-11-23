// The desk camera lives outside React: it changes every frame during pan / pinch, so it writes the
// world transform straight to the DOM and only notifies subscribers (zoom label, menus) once per frame.
import { clamp, type Rect } from './geometry';

export const MIN_Z = 0.1;
export const MAX_Z = 3;

export interface Cam { x: number; y: number; z: number }

export class Camera implements Cam {
  x = 0;
  y = 0;
  z = 0.5;
  world: HTMLElement | null = null;
  viewport: HTMLElement | null = null;
  private subs = new Set<() => void>();
  private frame = 0;
  private flight = 0;

  attach(viewport: HTMLElement | null, world: HTMLElement | null) {
    this.viewport = viewport;
    this.world = world;
    this.apply();
  }

  set(next: Partial<Cam>, stopFlight = true) {
    if (stopFlight) this.stop();
    if (next.x != null) this.x = next.x;
    if (next.y != null) this.y = next.y;
    if (next.z != null) this.z = clamp(next.z, MIN_Z, MAX_Z);
    this.apply();
    if (!this.frame) {
      this.frame = requestAnimationFrame(() => {
        this.frame = 0;
        this.subs.forEach((f) => f());
      });
    }
  }

  private apply() {
    if (this.world) this.world.style.transform = `translate3d(${this.x}px, ${this.y}px, 0) scale(${this.z})`;
    this.viewport?.style.setProperty('--z', String(this.z));
  }

  subscribe(fn: () => void) {
    this.subs.add(fn);
    return () => { this.subs.delete(fn); };
  }

  size() {
    return { w: this.viewport?.clientWidth || 1, h: this.viewport?.clientHeight || 1 };
  }

  // client (screen) point → world point
  toWorld(clientX: number, clientY: number) {
    const r = this.viewport?.getBoundingClientRect() ?? { left: 0, top: 0 };
    return { x: (clientX - r.left - this.x) / this.z, y: (clientY - r.top - this.y) / this.z };
  }

  // zoom keeping the screen point (sx, sy) — relative to the viewport — fixed
  zoomAt(z: number, sx: number, sy: number) {
    const nz = clamp(z, MIN_Z, MAX_Z);
    const wx = (sx - this.x) / this.z;
    const wy = (sy - this.y) / this.z;
    this.set({ z: nz, x: sx - wx * nz, y: sy - wy * nz });
  }

  zoomBy(f: number) {
    const { w, h } = this.size();
    this.zoomAt(this.z * f, w / 2, h / 2);
  }

  // camera that shows rect, leaving room for the toolbar
  forRect(rect: Rect, maxZ = 1): Cam {
    const { w, h } = this.size();
    const padX = Math.min(70, w * 0.06);
    const top = 30;
    const bottom = 100;
    const z = clamp(Math.min((w - padX * 2) / rect.w, (h - top - bottom) / rect.h), MIN_Z, maxZ);
    return { z, x: (w - rect.w * z) / 2 - rect.x * z, y: top + (h - top - bottom - rect.h * z) / 2 - rect.y * z };
  }

  stop() {
    cancelAnimationFrame(this.flight);
    this.flight = 0;
  }

  flyTo(target: Cam, ms = 460, onDone?: () => void) {
    this.stop();
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { this.set(target); onDone?.(); return; }
    const from = { x: this.x, y: this.y, z: this.z };
    const t0 = performance.now();
    const step = (now: number) => {
      const t = Math.min(1, (now - t0) / ms);
      const e = 1 - (1 - t) ** 3;
      this.set({ x: from.x + (target.x - from.x) * e, y: from.y + (target.y - from.y) * e, z: from.z + (target.z - from.z) * e }, false);
      if (t < 1) this.flight = requestAnimationFrame(step);
      else { this.flight = 0; onDone?.(); }
    };
    this.flight = requestAnimationFrame(step);
  }
}
