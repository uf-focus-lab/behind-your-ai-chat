<script setup lang="ts">
// CLIP's one idea, measured: four photographs and four captions, each a
// single 512-vector in the same space, and the cosine between every pair.
// The diagonal wins every row and every column. From demo/lib/figures/clip.py.
import Stage from '../../components/Stage.vue'
import data from '../../assets/vlfm/clip-matrix.json'

const thumbs = import.meta.glob<string>('../../assets/vlfm/*.webp', { eager: true, import: 'default', query: '?url' })
const src = (name: string) => thumbs[`../../assets/vlfm/${name}.webp`]

const all = data.cosine.flat()
const lo = Math.min(...all), hi = Math.max(...all)
const heat = (x: number) => (x - lo) / (hi - lo)
const best = data.cosine.map((row) => row.indexOf(Math.max(...row)))
</script>

<template>
  <Stage>
    <table class="vlfm-clip">
      <thead>
        <tr>
          <th class="vlfm-clip-corner"><span class="vlfm-clip-dim">cosine of two {{ data.dim }}-vectors</span></th>
          <th v-for="name in data.images" :key="name"><img :src="src(name)" class="vlfm-clip-thumb" :alt="name" /></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(caption, r) in data.captions" :key="caption">
          <th class="vlfm-clip-cap">{{ caption }}</th>
          <td v-for="(x, c) in data.cosine[r]" :key="c" :class="{ best: best[r] === c }" :style="{ '--h': heat(x) }">{{ x.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </Stage>
</template>

<style scoped>
.vlfm-clip { border-collapse: separate; border-spacing: 6px; }
.vlfm-clip th, .vlfm-clip td { padding: 0; font-weight: 400; }
.vlfm-clip-corner { text-align: left; vertical-align: bottom; }
.vlfm-clip-dim { font-size: 16px; color: var(--ink-faint); }
.vlfm-clip-thumb { display: block; width: 104px; height: 104px; border-radius: 6px; object-fit: cover; }
.vlfm-clip-cap { text-align: right; padding-right: 0.8rem !important; font-size: 21px; line-height: 1.25; color: var(--ink-strong); width: 320px; }
.vlfm-clip td {
  width: 104px; height: 60px;
  text-align: center;
  font-size: 22px;
  font-variant-numeric: tabular-nums;
  color: var(--ink);
  border-radius: 6px;
  background: color-mix(in srgb, var(--accent) calc(var(--h) * 55%), var(--paper));
}
.vlfm-clip td.best { color: var(--ink-strong); font-weight: 600; outline: 2px solid var(--accent); outline-offset: -2px; }
</style>
