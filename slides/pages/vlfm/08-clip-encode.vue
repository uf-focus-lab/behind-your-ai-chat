<script setup lang="ts">
// CLIP in four calls, the way clip.py makes them: a sentence and a photograph
// each become one vector of 512 numbers, and the cosine between the two is
// the whole model. Caption, token count and score come from
// demo/lib/figures/clip.py on CLIP ViT-B/32 and the dog.
import Stage from '../../components/Stage.vue'
import photo from '../../assets/vlfm/dog_a-square.webp'
import pair from '../../assets/vlfm/clip-pair.json'

const cos = pair.cosine.toFixed(3)
</script>

<template>
  <Stage gap="1.4rem">
    <div class="vlfm-enc-cols">
      <div class="vlfm-enc-col text">
        <h3>Text encoding</h3>
        <p class="vlfm-enc-code"><b>tokens</b> = tokenize(<i>"{{ pair.caption }}"</i>)</p>
        <p class="vlfm-enc-ret"><span class="vlfm-enc-down" aria-hidden="true" />{{ pair.tokens }} tokens</p>
        <p class="vlfm-enc-code"><b>vector</b> = encode_text(<b>tokens</b>)</p>
        <p class="vlfm-enc-ret"><span class="vlfm-enc-down" aria-hidden="true" />512 numbers</p>
        <p class="vlfm-enc-got">the sentence as 512 numbers</p>
      </div>
      <div class="vlfm-enc-col image">
        <h3>Image encoding</h3>
        <p class="vlfm-enc-code"><b>pixels</b> = preprocess(<img :src="photo" class="vlfm-enc-thumb" alt="the dog" />)</p>
        <p class="vlfm-enc-ret"><span class="vlfm-enc-down" aria-hidden="true" />{{ pair.pixels }} × {{ pair.pixels }} pixels</p>
        <p class="vlfm-enc-code"><b>vector</b> = encode_image(<b>pixels</b>)</p>
        <p class="vlfm-enc-ret"><span class="vlfm-enc-down" aria-hidden="true" />512 numbers</p>
        <p class="vlfm-enc-got">the picture as 512 numbers</p>
      </div>
    </div>
    <!-- The two vectors meet: a curved sweep rises from the score to the last
         line of each column. Both arcs are one element each - a box with two
         borders and an elliptical corner - plus a triangle for the head, so
         the figure stays CSS and inherits the ink tokens in both schemes. -->
    <div class="vlfm-enc-join">
      <span class="vlfm-enc-sweep left" aria-hidden="true" />
      <p class="vlfm-enc-cos">similarity <b>{{ cos }}</b></p>
      <span class="vlfm-enc-sweep right" aria-hidden="true" />
    </div>
  </Stage>
</template>

<style scoped>
.vlfm-enc-cols { display: flex; width: 100%; }
.vlfm-enc-col { min-width: 0; display: flex; flex-direction: column; gap: 0.7rem; }
.vlfm-enc-col.text { flex: 1.06 1 0; padding-right: 1.4rem; }
.vlfm-enc-col.image { flex: 0.94 1 0; padding-left: 1.4rem; border-left: 1px solid var(--ink-hair); }
.vlfm-enc-col h3 { margin: 0 0 0.3rem; font-size: 30px; font-weight: 600; color: var(--ink-strong); }
.vlfm-enc-col p { margin: 0; }

/* A fixed line box, tall enough for the thumbnail in the image column, so
   the two columns keep the same rhythm line for line. */
.vlfm-enc-code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 19px; line-height: 38px; color: var(--ink-strong); white-space: nowrap; }
.vlfm-enc-code b { font-weight: 600; color: var(--accent); }
.vlfm-enc-code i { font-style: normal; color: var(--ink); }
.vlfm-enc-thumb { display: inline-block; width: 36px; height: 36px; margin: -4px 0; border-radius: 5px; vertical-align: -11px; }

.vlfm-enc-ret { display: flex; align-items: center; gap: 0.5rem; padding-left: 0.5rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 18px; color: var(--ink-faint); }
/* A drawn down arrow instead of the glyph: a stem the weight of the sweeps
   with a triangular head, so the two arrow kinds on the slide match. */
.vlfm-enc-down { position: relative; width: 11px; height: 24px; flex: none; }
.vlfm-enc-down::before { content: ""; position: absolute; left: 4.5px; top: 0; width: 2px; height: 15px; background: var(--ink-faint); }
.vlfm-enc-down::after { content: ""; position: absolute; left: 0; bottom: 0; border-left: 5.5px solid transparent; border-right: 5.5px solid transparent; border-top: 10px solid var(--ink-faint); }

.vlfm-enc-got { margin-top: 0.3rem !important; font-size: 27px; line-height: 1.25; color: var(--ink-strong); }

.vlfm-enc-join { display: flex; align-items: flex-end; gap: 1rem; }
.vlfm-enc-sweep { position: relative; flex: none; width: 180px; height: 62px; margin-bottom: 19px; border: 0 solid var(--ink-faint); }
.vlfm-enc-sweep.left { border-left-width: 2.5px; border-bottom-width: 2.5px; border-bottom-left-radius: 100% 100%; }
.vlfm-enc-sweep.right { border-right-width: 2.5px; border-bottom-width: 2.5px; border-bottom-right-radius: 100% 100%; }
.vlfm-enc-sweep::after { content: ""; position: absolute; top: -8px; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 9px solid var(--ink-faint); }
.vlfm-enc-sweep.left::after { left: -7.25px; }
.vlfm-enc-sweep.right::after { right: -7.25px; }

p.vlfm-enc-cos { margin: 0; font-size: 32px; line-height: 1.3; color: var(--ink); white-space: nowrap; }
p.vlfm-enc-cos b { font-weight: 600; color: var(--accent); font-variant-numeric: tabular-nums; }
</style>
