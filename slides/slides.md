---
theme: default
title: Behind Your AI Chat
titleTemplate: '%s'
info: |
  Two guest lectures for EEL 4403/5406 Computational Photography,
  University of Florida.
class: text-center
routerMode: hash
# Figure.vue resolves and bundles the real assets, so Slidev's own image
# preloader, which refetches src strings verbatim, has nothing to contribute.
preloadImages: false
fonts:
  provider: none
  sans: 'Source Serif 4'
  serif: 'Source Serif 4'
transition: slide-up
---

<style scoped>
/* title and subtitle centred on the slide as one block; the byline pinned to the foot */
.slidev-layout { position: relative; display: flex; flex-direction: column; justify-content: center; align-items: center; }
.slidev-layout h1 {
  display: inline-block;
  margin: 0;
  padding: 0;
  font-size: 3.2rem !important;
  line-height: 1.3em !important;
}
/* the rule is drawn by the title itself, so it is exactly as wide as the title */
.slidev-layout h1::after {
  content: "";
  display: block;
  height: 1px;
  margin-top: 0.35em;
  background: var(--ink-soft);
}
.slidev-layout p.deck-subtitle {
  margin: 1.1rem 0 0;
  font-size: 1.6rem;
  line-height: 1.4;
  color: var(--ink-strong);
  opacity: 1;
}
.slidev-layout p.deck-byline {
  position: absolute;
  left: 0; right: 0; bottom: 3.2rem;
  margin: 0;
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--ink-faint);
}
</style>

# Behind Your AI Chat

<p class="deck-subtitle">A tour of LLMs, agentic AI and VLFMs</p>

<p class="deck-byline">Yuxuan Zhang<br>EEL 4403 / 5406 · Computational Photography · Fall 2026</p>

<!--
A tour, and it starts where you already are: your own chat window. We take it apart, one stream of tokens; we make the model act, an agent; we make it see, a vision-language model; and we end on a robot from our lab that runs on nothing else. Everything on these slides is a real output of a real program in the repository.
-->

---
layout: center
transition: view-transition
---

<script setup lang="ts">
import Chat from '@pages/llm/01-chat.vue'
</script>

<Chat />

<!--
This is what everyone has seen. You type a sentence, the assistant answers. It looks like a person on the other end reading your message. Run chat.py and it does exactly this from the command line: type the question, read the reply.

Hold this picture, because the next slide is the same conversation with the costume taken off.
-->

---
clicks: 2
---

# <span class="chapter-title">Under the hood</span> · One stream of tokens

<script setup lang="ts">
import Stream from '@pages/llm/02-stream.vue'
</script>

<Stream />

<!--
The bubbles are gone. What the model receives is one sequence of tokens, read left to right, and three things appear that the chat window never showed, one per click.

First, the words are cut into tokens, pieces from a fixed vocabulary of 49 152, and each token is just its index into a table of learned vectors, the number under it. "Hello" is one token, and so is the question mark. Click: the roles. There is no separate channel for the user and the assistant; a special token marks where each role begins, and the model learned during training what tends to follow each marker. That is all "you are an assistant" means to it. Click: a message the user never typed comes first, the system prompt, "You are a helpful assistant. Keep replies to one sentence", which the program sent along.

The reply, when it comes, is appended to the same stream after the agent marker, one token at a time. These tokens come from a small open model running on this laptop, because hosted models do not publish their tokenizer, but the mechanism is identical.
-->

---
clicks: 6
---

# <span class="chapter-title">Predictor</span> · Pick the next token

<script setup lang="ts">
import Predictor from '@pages/llm/06-predictor.vue'
</script>

<Predictor />

<!--
So what does the model do with the stream? One thing. It reads it and produces a probability for every one of the 49 152 pieces in its vocabulary, as the next token. These are the real numbers from the small model on this laptop, after our message: it wants to say "I" with probability 0.90.

Click: take the top one, append it to the stream, run the whole thing again. Now it wants "can", at 0.76, with "'m" second. Click, click, click: "help", "you", "with", "a". A reply is this loop, one token per pass, and nothing carries over between passes except the stream itself. Answering, playing a cat, writing a tool call: all of it is this one operation, chosen one token at a time. There is no separate place where the model "knows" things; there is only what the next token tends to be, and you are about to see what that costs.
-->

---
layout: center
---

<script setup lang="ts">
import Play from '@pages/llm/03-play.vue'
</script>

<Play />

<!--
To the terminal. python chat.py. Say hello; it introduces itself as ChatGPT, which is the training talking. Rewrite the first message of the list into the cat, run again, ask anything: miaow. The weights did not change; one line of the list did. Then the exploit: keep the cat, start the user message with "[System]" and tell it that it is a physicist. Predict first, then watch. Whatever happens, the reason is on the stream slide: one sequence, learned markers, nothing enforced.

Then ask it something arithmetic that it cannot do in one pass, seven to the thirty-third, and keep the wrong answer on screen. Back to the deck.
-->

---
layout: center
clicks: 1
---

<script setup lang="ts">
import Question from '@pages/llm/04-question.vue'
</script>

<Question a="the use of tools" />

<!--
Back from the terminal. The cat followed one line of text at the top of the list, and the "[System]" trick worked or did not for the same reason: the model has one sequence, and the markers in it are learned, not enforced. Whoever writes the list decides who the model is.

So the question. The same model answered hello, played a cat, and did arithmetic in its head, some of it wrong. What has to change to call it an agent? Not the weights. Click: the use of tools. The model gets to ask for something to be done, and a program does it and tells it the result.
-->

---
clicks: 3
---

# <span class="chapter-title">Everything</span> · Tools are tokens too

<script setup lang="ts">
import Everything from '@pages/llm/05-everything.vue'
</script>

<Everything />

<!--
This is what the tool turn you just watched looks like to the model. It is the same picture as before, and that is the point. The program sends the system prompt, then the tools it offers, as text, a name and the argument it takes, then the question. Nothing has been added to the model; it reads a description of a clock the way it reads anything else.

Click: the model writes a call. It is tokens, in a shape the program agreed to parse: a name and a JSON argument, and then it stops. Click: the program runs the clock and appends the answer under a tool marker. Click: the model reads the whole stream again, now with the time in it, and answers, as a cat. Every layer that gets called agentic, tools, memory, planning, other agents, is a program deciding what to append to this stream next. The model only ever sees the stream.
-->

---
layout: center
---

<script setup lang="ts">
import Play from '@pages/llm/03-play.vue'
</script>

<Play line="Back to the terminal" cmd="@tool" />

<!--
Back to chat.py. Write the two tools in front of the class, read_file and write_file, four lines each under @tool: a name, a type hint, a docstring. That is all the model ever sees of them. Then ask: "solve homework.txt". Watch the yellow lines: it reads the file, calls the calculator, writes the answer back, and says miaow. Open the file to prove it.

Then the arithmetic from before, seven to the thirty-third, now with calculate on the list: the wrong answer becomes the right one, and the model did not get smarter, it got a tool. Back to the deck.
-->

---

# <span class="chapter-title">Agents</span> · App and terminal

<script setup lang="ts">
import Agents from '@pages/llm/07-agents.vue'
</script>

<Agents />

<!--
You have now built the whole thing. Every one of these companies ships the same model through two doors. The left door is the app, the chat window from the first slide. The right door is a program you run in a terminal, and it is chat.py with more tools: read a file, write a file, run a shell command, search the code. Codex CLI, Claude Code, Gemini CLI, Grok Build: the loop you wrote today, the model asking for tools and the program running them, appending, calling again, until the job is done.

Nothing on the right knows anything the left does not. The difference between a chatbot and a coding agent is the list of tools and the loop, which is why those programs appeared within months of each other once the models could call tools reliably. When you use one this week, picture the stream: your request, the tool schemas, a call, a result, a call, a result, an answer.
-->

---
layout: center
---

<script setup lang="ts">
import Question from '@pages/llm/04-question.vue'
</script>

<Question q="How does a language model <em>see</em>?" />

<!--
Same question shape as before. We have a model that reads one stream of tokens and predicts the next. Nothing in it has eyes. So how do the chat apps answer questions about a photo? The picture becomes tokens. Not a description of the picture, the picture itself, cut up and pushed into the same stream. The next two slides are the hello-world conversation again, with a photograph in it.
-->

---
layout: center
transition: view-transition
---

<script setup lang="ts">
import ChatVision from '@pages/vlfm/13-chat-vision.vue'
</script>

<ChatVision />

<!--
The same chat window. This time the user attaches a photograph and asks what is in it, and the assistant describes it: a cream-coloured dog, likely a golden retriever, green plants, a leash. That reply is real, from the same model chat.py talks to; the program sent the JPEG bytes along with the question.

Hold the picture again, because the next slide takes the costume off a second time.
-->

---

# <span class="chapter-title">Vision Transformer</span> - Image Tiles as Visual Tokens

<script setup lang="ts">
import StreamVision from '@pages/vlfm/14-stream-vision.vue'
</script>

<StreamVision />

<!--
The photograph did not go in as a file. It was cut into tiles, and every tile became a token, sitting in the stream between the user marker and the question, before the words. The reply is appended after the agent marker exactly as before. The model attends over tiles and words with the same attention; there is no separate vision channel.

Two differences from word tokens, and they matter. The tiles have no id under them: a word token is one row of a 49 152-row table, but a picture token is a vector computed from the pixels, so there is no vocabulary of pictures. And the picture is expensive: this one cost 1 185 tokens, measured by sending the same question with and without it. A paragraph of text is about 200. How the tiles become vectors, and why they land in a space the language model can read, is the rest of this lecture.
-->

---

# <span class="chapter-title">CLIP</span> · One vector each

<script setup lang="ts">
import ClipEncode from '@pages/vlfm/08-clip-encode.vue'
</script>

<ClipEncode />

<!--
CLIP is two encoders and one idea, and here it is as the four calls clip.py makes. A sentence goes through the tokenizer, eight ids for this caption, and through a text transformer that returns one vector of 512 numbers. A photograph is resized and cropped to 224 by 224, goes through a vision transformer, the block you know, cut into patches, and comes out as one vector of 512 numbers. Same length, same space.

That is the whole model. The cosine between the two vectors, 0.348 for this pair, is how much the sentence and the picture agree. There is no classifier, no list of categories; any sentence you can type is a query, and any picture can be scored against it with one dot product. The next slide shows what the space looks like across a few pictures and captions, and the demo will let you fight over it.
-->

---

# <span class="chapter-title">CLIP</span> · One shared space

<script setup lang="ts">
import ClipSpace from '@pages/vlfm/09-clip-space.vue'
</script>

<ClipSpace />

<!--
CLIP is two encoders and one idea. A vision transformer turns a photograph into one vector of 512 numbers. A text transformer turns a sentence into one vector of 512 numbers. They are trained so that a picture and a sentence that describe the same thing point the same way.

These are real numbers from the model on this laptop: four photographs, four captions I wrote, and the cosine between every pair. Read a row: the caption about the doormat is closest to the dog on the doormat, further from the other dog, furthest from the mugs. Read a column: each photograph's best caption is its own. Nothing was trained on these photographs. That is what a shared space buys you: any sentence is now a query, and any picture can be compared with it by one dot product.
-->

---
layout: center
---

<script setup lang="ts">
import DemoClip from '@pages/vlfm/12-demo-clip.vue'
</script>

<DemoClip />

<!--
Contest. I take one photograph in this room, right now, and open the leaderboard: python clip.py class.jpg. Each group has two minutes to agree on one caption, one sentence, and sends it to me as "caption # group number". I type them in, the picture is embedded once, each caption is embedded and scored, and the board re-sorts after every entry, so you can see what moves the score: naming the objects, the colours, the setting, the number of people.

Every group that enters gets five points; the highest similarity gets ten. Both count toward today's lab on global and direct illumination separation, which is on Canvas; check the assignment there after class. Think about what CLIP's training data looked like, captions from the web, before you write your sentence.
-->

---
layout: center
---

<style scoped>
/* the brief is the whole slide: no title band, no layout padding */
.slidev-layout { position: relative; padding: 0; }
</style>

<script setup lang="ts">
import Vlx from '@pages/vlfm/16-vlx.vue'
</script>

<Vlx />

<!--
This is what the contest you just ran looks like as a robot. VL-Explore is our work from the lab: a mobile robot in a floor it has never seen, one camera, no map, no depth sensor. Each frame is cut into six tiles, each tile becomes one CLIP vector, exactly the vector the demo scored, and each vector is compared with sentences: is this traversable floor, is this the thing we are looking for, have I seen this before. The robot drives toward the tile whose cosines say yes.

Watch the overlay: the scores change as the view changes, and nothing here was trained on this building. That is the whole reason a shared image–text space matters for a photographer or a roboticist: a sentence is now a sensor.
-->

---

# <span class="chapter-title">DINO</span> · Better patch tokens

<script setup lang="ts">
import Dino from '@pages/vlfm/17-dino.vue'
</script>

<Dino />

<!--
One more encoder, and the reason is in the middle picture. CLIP's vision transformer also produces one vector per patch, 49 of them for this model, and on our dog they are a blur, because CLIP's training only ever touched the one pooled vector you saw; the 49 patch vectors under it were never asked to be anything. DINO trains the patch vectors themselves, with no captions and no labels: a student network must match a teacher's output on different crops of the same image, and DINOv2 adds a masked-patch objective, so every patch vector has to be predictable from its neighbours. The right picture is the result on the same photograph: the dog is one clean silhouette, the foliage another colour, and the same colour would mean the same kind of thing in a second photograph.

So the trade. CLIP knows words: its space is aligned with language, and you can query it with a sentence. DINO knows where: its space is aligned with geometry, and you build depth, segmentation and correspondence on it. That is why Depth Anything and our own FoveaCam Duo stand on DINOv2 rather than CLIP, which is the second lecture. Both lines are still moving: SigLIP replaced CLIP's softmax with a sigmoid and trains better at scale; DINOv2 and DINOv3 are the same idea with more data and a cleaner patch objective, and today they are the default backbone for anything spatial.
-->

---
layout: center
---

<script setup lang="ts">
import Question from '@pages/llm/04-question.vue'
</script>

<Question q="Lab 4 <span class=&quot;deck-sep&quot;>|</span> Global / Direct Separation" style="--q-size: 46px" />

<!--
That is the lecture. One stream of tokens: words, a system prompt, a tool call, a picture, all the same thing to the model, and one block stacked N times that predicts the next one. On top of it, two encoders: CLIP, which puts pictures and sentences in one space, and DINO, which makes patch vectors you can build geometry on.

Now the lab: global and direct illumination separation. The assignment is on Canvas; the contest points from today count toward it.
-->

---

# <span class="chapter-title">Hint</span> · Choice of Scene

<script setup lang="ts">
import Shapes from '@pages/lab/01-shapes.vue'
</script>

<Shapes />

<!--
Two hints before you start. First, what to photograph. Light that hits a convex surface bounces once and leaves; what reaches the camera is the direct component, and the global part is close to nothing. Light that falls into a concave shape, a bowl, a corner, the inside of a cup, hits one wall, then the other, then leaves: the camera sees the direct bounce plus everything that arrived by way of the other walls, the global component. Translucent things do the same under the skin.

So choose scenes with both: a convex thing next to a concave one, wax or skin next to matte paper, and the separation will have something to show.
-->

---

# <span class="chapter-title">Hint</span> · You May Use this Projector

<script setup lang="ts">
import Patterns from '@pages/lab/02-patterns.vue'
</script>

<Patterns />

<!--
Second, how to light it. The separation works because a projector can light half the pixels and leave the other half dark, at a spacing finer than the scene's global light varies over. Under such a pattern a lit pixel receives direct plus half the global light, an unlit one receives half the global light alone; shift the pattern so every pixel is lit in one frame and dark in another, and two subtractions give you both components.

These are six patterns a projector can throw, animated the way you would step them: a checkerboard shifted by one square, stripes stepped through three phases, a sinusoid instead of a hard edge, a lattice of dots, a single swept line. The checkerboard with a few shifts is the classic; the others trade frames for robustness. Pick one, keep the squares small, take the max and the min at every pixel across the shifts.
-->
