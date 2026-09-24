<script setup lang="ts">
// The same model behind two doors: the chat app everyone has seen, and the
// command-line coding agent each vendor ships, which is the loop from
// chat.py with tools for files and a shell. U.S. vendors with their own models.
//
// The four commands share one dark panel so the right half reads as a single
// terminal session, four prompts aligned on their `$`. Its colours are fixed,
// not theme tokens: a terminal is dark in both schemes. `plate` marks the icon
// whose own tile is black, so it keeps an edge on dark paper. (Not `ring`:
// that is a Uno utility and would paint its own blue halo.)
import Stage from '../../components/Stage.vue'
import ChatGPT from '../../assets/agents/chatgpt.svg'
import Claude from '../../assets/agents/claude.svg'
import Gemini from '../../assets/agents/gemini.svg'
import Grok from '../../assets/agents/grok.svg'

const rows = [
  { app: 'ChatGPT', mark: ChatGPT, cli: 'codex', agent: 'Codex CLI', vendor: 'OpenAI' },
  { app: 'Claude', mark: Claude, cli: 'claude', agent: 'Claude Code', vendor: 'Anthropic' },
  { app: 'Gemini', mark: Gemini, cli: 'gemini', agent: 'Gemini CLI', vendor: 'Google' },
  { app: 'Grok', mark: Grok, cli: 'grok', agent: 'Grok Build', vendor: 'xAI', plate: true },
]
</script>

<template>
  <Stage>
    <div class="llm-agents">
      <span class="llm-agents-head llm-agents-head-app">the app</span>
      <span class="llm-agents-head llm-agents-head-cli">the coding agent</span>
      <div class="llm-agents-term" />
      <template v-for="(r, i) in rows" :key="r.cli">
        <div class="llm-agents-app" :style="{ gridRow: i + 2 }">
          <component :is="r.mark" class="llm-agents-mark" :class="{ plate: r.plate }" />
          <span class="llm-agents-name">{{ r.app }}</span>
        </div>
        <span class="llm-agents-eq" :style="{ gridRow: i + 2 }">&#8801;</span>
        <div class="llm-agents-line" :style="{ gridRow: i + 2 }">
          <span class="llm-agents-prompt">$</span><span class="llm-agents-cmd">{{ r.cli }}</span>
        </div>
        <span class="llm-agents-agent" :style="{ gridRow: i + 2 }">{{ r.agent }} · {{ r.vendor }}</span>
      </template>
    </div>
  </Stage>
</template>

<style scoped>
.llm-agents {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 250px 64px 214px 1fr;
  grid-template-rows: auto repeat(4, 1fr);
  column-gap: 24px;
}
.llm-agents-head {
  grid-row: 1;
  font-size: 17px;
  font-variant: small-caps;
  letter-spacing: 0.04em;
  color: var(--ink-faint);
  padding-bottom: 0.25rem;
  margin-bottom: 0.9rem;
  border-bottom: 1px solid var(--ink-hair);
}
.llm-agents-head-app { grid-column: 1 / 3; }
.llm-agents-head-cli { grid-column: 3 / -1; }

/* The terminal ground, laid behind the four command rows. */
.llm-agents-term {
  grid-column: 3;
  grid-row: 2 / -1;
  background: #1b1e23;
  border: 1px solid #3a3f47;
  border-radius: 12px;
}

.llm-agents-app { grid-column: 1; display: flex; align-items: center; gap: 1rem; }
.llm-agents-mark { height: 56px; width: 56px; flex: none; border-radius: 12px; }
.dark .llm-agents-mark.plate { box-shadow: 0 0 0 1px var(--ink-dim); }
.llm-agents-name { font-size: 34px; font-weight: 600; color: var(--ink-strong); }

.llm-agents-eq {
  grid-column: 2;
  /* Identical-to, not equals: small and grey, so it reads as a quiet
     mathematical sign rather than a sum or a menu icon. */
  font-size: 24px;
  color: var(--ink-dim);
  text-align: center;
  align-self: center;
}

.llm-agents-line {
  grid-column: 3;
  align-self: center;
  padding-left: 1.6rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 30px;
  line-height: 1.1;
  color: #ececec;
}
.llm-agents-prompt { color: #5bb3ff; margin-right: 0.6em; }

.llm-agents-agent {
  grid-column: 4;
  align-self: center;
  font-size: 20px;
  color: var(--ink-faint);
  white-space: nowrap;
}
</style>
