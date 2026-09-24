<script setup lang="ts">
// Two ray diagrams for the lab, traced rather than drawn: parallel light
// from above meets a circular bump or a circular bowl and reflects by the
// law of reflection. On the bump every ray leaves after one bounce, so the
// camera sees direct light; in the bowl a ray's first bounce lands on the
// far wall, and what leaves after that second bounce is global light.
import Stage from '../../components/Stage.vue'

type V = [number, number]
const add = (a: V, b: V, k = 1): V => [a[0] + k * b[0], a[1] + k * b[1]]
const sub = (a: V, b: V): V => [a[0] - b[0], a[1] - b[1]]
const dot = (a: V, b: V) => a[0] * b[0] + a[1] * b[1]
const norm = (a: V): V => { const l = Math.hypot(a[0], a[1]); return [a[0] / l, a[1] / l] }

// first hit of the ray p + t·d on the circle (c, r), or null
function hit(p: V, d: V, c: V, r: number, keep: (q: V) => boolean): V | null {
  const f = sub(p, c)
  const b = dot(f, d), cc = dot(f, f) - r * r
  const disc = b * b - cc
  if (disc < 0) return null
  const ts = [-b - Math.sqrt(disc), -b + Math.sqrt(disc)].filter((t) => t > 1e-3)
  for (const t of ts) { const q = add(p, d, t); if (keep(q)) return q }
  return null
}
const reflect = (d: V, n: V): V => add(d, n, -2 * dot(d, n))
const seg = (a: V, b: V) => `M ${a[0].toFixed(1)} ${a[1].toFixed(1)} L ${b[0].toFixed(1)} ${b[1].toFixed(1)}`

// the bump: a semicircle standing on the floor at y = 200
const bump = { c: [180, 200] as V, r: 90 }
const convex = [110, 145, 180, 215, 250].map((x) => {
  const p: V = [x, 18], d: V = [0, 1]
  const q = hit(p, d, bump.c, bump.r, (q) => q[1] <= bump.c[1])!
  const out = reflect(d, norm(sub(q, bump.c)))
  return { direct: [seg(p, q), seg(q, add(q, out, 120))], end: add(q, out, 120) }
})

// the bowl: a semicircle hanging from the rim at y = 60
const bowl = { c: [180, 60] as V, r: 90 }
const concave = [128, 160, 205, 240].map((x) => {
  const p: V = [x, 6], d: V = [0, 1]
  const inBowl = (q: V) => q[1] >= bowl.c[1]
  // follow the ray through up to three bounces inside the bowl
  const path: V[] = [hit(p, d, bowl.c, bowl.r, inBowl)!]
  let dir = reflect(d, norm(sub(bowl.c, path[0])))
  for (let bounce = 0; bounce < 3; bounce++) {
    const q = hit(path[path.length - 1], dir, bowl.c, bowl.r, inBowl)
    if (!q) break
    path.push(q)
    dir = reflect(dir, norm(sub(bowl.c, q)))
  }
  const last = path[path.length - 1], end = add(last, dir, 130)
  // one hit: the ray leaves after a single bounce, direct light; more hits:
  // everything after the first bounce is global
  const direct = [seg(p, path[0])]
  const global: string[] = []
  if (path.length === 1) direct.push(seg(path[0], end))
  else {
    for (let i = 1; i < path.length; i++) global.push(seg(path[i - 1], path[i]))
    global.push(seg(last, end))
  }
  return { direct, global, end }
})
</script>

<template>
  <Stage row gap="3rem">
    <figure class="lab-shape">
      <svg viewBox="0 0 360 240" class="lab-shape-svg" aria-label="a convex bump lit from above; each ray leaves after one bounce">
        <defs><pattern id="hatch-bump" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" class="hatch" /></pattern></defs>
        <path d="M 20 200 H 90 A 90 90 0 0 1 270 200 H 340 V 234 H 20 Z" class="solid" fill="url(#hatch-bump)" />
        <path d="M 20 200 H 90 A 90 90 0 0 1 270 200 H 340" class="surface" />
        <g class="direct"><path v-for="(r, i) in convex" :key="i" :d="r.direct.join(' ')" /></g>
        <g class="tips"><circle v-for="(r, i) in convex" :key="i" :cx="r.end[0]" :cy="r.end[1]" r="3" /></g>
      </svg>
      <figcaption>convex</figcaption>
    </figure>
    <figure class="lab-shape">
      <svg viewBox="0 0 360 240" class="lab-shape-svg" aria-label="a concave bowl lit from above; rays bounce between its walls before leaving">
        <defs><pattern id="hatch-bowl" patternUnits="userSpaceOnUse" width="10" height="10" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="10" class="hatch" /></pattern></defs>
        <path d="M 20 60 H 90 A 90 90 0 0 0 270 60 H 340 V 234 H 20 Z" class="solid" fill="url(#hatch-bowl)" />
        <path d="M 20 60 H 90 A 90 90 0 0 0 270 60 H 340" class="surface" />
        <g class="direct"><path v-for="(r, i) in concave" :key="i" :d="r.direct.join(' ')" /></g>
        <g class="global"><path v-for="(r, i) in concave" :key="i" :d="r.global.join(' ')" /></g>
        <g class="tips"><circle v-for="(r, i) in concave" :key="i" :cx="r.end[0]" :cy="r.end[1]" r="3" :class="{ acc: r.global.length }" /></g>
      </svg>
      <figcaption>concave</figcaption>
    </figure>
  </Stage>
</template>

<style scoped>
.lab-shape { margin: 0; width: 400px; display: flex; flex-direction: column; align-items: center; gap: 0.6rem; }
.lab-shape-svg { width: 400px; height: 266px; overflow: visible; }
.lab-shape-svg path:not(.solid) { fill: none; stroke-linecap: round; stroke-linejoin: round; }
.lab-shape-svg .solid { stroke: none; }
.lab-shape-svg .surface { stroke: var(--ink-strong); stroke-width: 4; }
.lab-shape-svg .direct path { stroke: var(--ink); stroke-width: 2; }
.lab-shape-svg .global path { stroke: var(--accent); stroke-width: 2.5; }
.lab-shape-svg .tips circle { fill: var(--ink); }
.lab-shape-svg .tips circle.acc { fill: var(--accent); }
.lab-shape figcaption { font-size: 26px; font-weight: 600; color: var(--ink-strong); text-align: center; }
.lab-shape-svg .hatch { stroke: var(--ink-soft); stroke-width: 1; }
</style>
