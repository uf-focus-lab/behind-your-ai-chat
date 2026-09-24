<script setup lang="ts">
// A question left in the air, and its answer on a click, or the question
// alone when no answer is given. The question may carry <em> for one
// stressed word.
//
//   <Question q="What makes an <em>agentic</em> AI?" a="the use of tools" />
import { useSlideContext } from '@slidev/client'
withDefaults(defineProps<{ q?: string; a?: string }>(), {
  q: 'What makes an <em>agentic</em> AI?',
  a: '',
})
const { $clicks } = useSlideContext()
</script>

<template>
  <div class="llm-question" :class="{ pending: a && $clicks < 1 }">
    <p class="llm-question-q" v-html="q" />
    <p v-if="a" class="llm-question-a" :class="{ shown: $clicks >= 1 }"><span class="llm-question-dash">—</span>{{ a }}</p>
  </div>
</template>

<style scoped>
.llm-question {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.6rem;
}
/* Before the answer, the question alone is centred: it sits shifted down by
   half the space the answer will take, and rises when the answer comes. */
p.llm-question-q {
  margin: 0;
  font-size: var(--q-size, 58px);
  line-height: 1.2;
  font-weight: 600;
  color: var(--ink-strong);
  text-align: center;
  text-wrap: balance;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.pending p.llm-question-q { transform: translateY(calc((48px + 1.6rem) / 2)); }
p.llm-question-q :deep(em) { font-style: italic; font-weight: 600; }
p.llm-question-a {
  margin: 0;
  font-size: 40px;
  line-height: 1.2;
  color: var(--accent);
  text-align: center;
  opacity: 0;
  transform: translateY(10px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
p.llm-question-a.shown { opacity: 1; transform: none; }
.llm-question-dash { margin-right: 0.35em; }
</style>
