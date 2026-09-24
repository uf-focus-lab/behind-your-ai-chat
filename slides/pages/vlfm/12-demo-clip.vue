<script setup lang="ts">
// The caption contest. One word on the left, the two point values on the
// right, "points" over the labels as their unit, and the terminal card that
// marks every demo slide beneath them; everything else is in the notes.
import Stage from '../../components/Stage.vue'
import Terminal from '../../components/Terminal.vue'
</script>

<template>
  <Stage gap="2.4rem" class="vlfm-contest">
    <div class="vlfm-contest-row">
      <p class="vlfm-contest-head">Contest!</p>
      <span class="vlfm-contest-rule" aria-hidden="true" />
      <div class="vlfm-contest-terms">
        <ul>
          <li><b>+5</b><span><small>points</small>participation</span></li>
          <li><b>+10</b><span><small>points</small>winner</span></li>
        </ul>
      </div>
    </div>
    <Terminal cmd="python clip.py class.jpg" width="620px" />
  </Stage>
</template>

<style scoped>
/* The `center` layout wraps the slide body in a shrink-to-fit block, so
   `width: 100%` on the Stage only ever measures its own content. The page
   claims the layout's full content band (980 minus its 56px side padding)
   explicitly, then spreads the word and the terms to its two edges. The
   selector has to out-specify Stage's own centring rule. */
.deck-stage.vlfm-contest {
  width: 868px;
  align-items: center;
}
.vlfm-contest-row { display: flex; justify-content: center; align-items: center; gap: 2.6rem; }
/* a rule between the word and the terms, as tall as the terms */
.vlfm-contest-rule { align-self: stretch; width: 1px; background: var(--ink-hair); }

p.vlfm-contest-head {
  margin: 0;
  flex: 0 0 auto;
  font-size: 92px;
  line-height: 1;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: -0.025em;
}

.vlfm-contest-terms {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.vlfm-contest-terms p { margin: 0; }

.vlfm-contest-terms ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
}
.vlfm-contest-terms li {
  display: grid;
  grid-template-columns: 106px 1fr;
  align-items: end;
  gap: 0.9rem;
  margin: 0;
}
.vlfm-contest-terms li b {
  font-size: 64px;
  line-height: 1;
  font-weight: 600;
  color: var(--ink-strong);
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.02em;
  text-align: right;
}
.vlfm-contest-terms li span {
  display: flex;
  flex-direction: column;
  font-size: 26px;
  line-height: 1.15;
  color: var(--ink);
}
.vlfm-contest-terms li small {
  font-size: 15px;
  font-variant: small-caps;
  letter-spacing: 0.04em;
  color: var(--ink-faint);
}
</style>
