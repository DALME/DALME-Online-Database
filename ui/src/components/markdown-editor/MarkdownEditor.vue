<template>
  <template v-if="editable">
    <q-card flat bordered :class="containerClasses">
      <div>
        <q-tabs v-model="mdTab" dense indicator-color="transparent" no-caps>
          <q-tab name="write" label="Write" />
          <q-tab name="preview" label="Preview" :disable="disabled" />
        </q-tabs>

        <MDEToolbar
          :dark="dark"
          @insert-enclosure="insertEnclosure"
          @insert-prefix="insertPrefix"
        />
      </div>

      <q-separator />
      <q-tab-panels
        v-model="mdTab"
        keep-alive
        animated
        transition-prev="jump-up"
        transition-next="jump-up"
      >
        <q-tab-panel name="write" class="q-pa-sm">
          <q-input
            type="textarea"
            ref="input"
            v-model="mdText"
            outlined
            dense
            :placeholder="pHolder"
            autocapitalize="off"
            autocomplete="off"
            autocorrect="off"
          />
        </q-tab-panel>
        <q-tab-panel name="preview" class="q-py-sm q-px-md">
          <q-markdown
            :class="dark ? 'dark' : ''"
            :src="mdText"
            :extend="extendMarkdown"
            style="min-height: 132px"
            task-lists-enable
          />
        </q-tab-panel>
      </q-tab-panels>

      <div class="md-editor-footer">
        <q-icon
          size="sm"
          name="mdi-language-markdown"
          @click="openMarkdown"
          class="cursor-pointer q-mr-sm"
        />
        <div v-if="help" class="text-caption">{{ help }}</div>
        <q-space />
        <q-btn
          class="submit-button text-roboto"
          :disable="disabled"
          :label="buttonLabel"
          @click="onSubmit"
        />
      </div>
    </q-card>
  </template>
  <q-markdown
    v-else
    :class="dark ? 'dark' : ''"
    :src="mdText"
    :extend="extendMarkdown"
    task-lists-enable
  />
</template>

<script>
import { openURL } from "quasar";
import { nully } from "@/utils";
import { computed, defineComponent, onMounted, provide, ref } from "vue";
import MDEToolbar from "./MDEToolbar.vue";

export default defineComponent({
  name: "MarkdownEditor",
  props: {
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
    right: {
      type: Boolean,
      required: false,
      default: false,
    },
    editable: {
      type: Boolean,
      required: false,
      default: false,
    },
    text: {
      type: String,
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
    help: {
      type: String,
      required: false,
    },
    submitLabel: {
      type: String,
      required: false,
    },
  },
  components: {
    MDEToolbar,
  },
  emits: ["onSaveText"],
  setup(props, context) {
    const textareaEl = ref(null);
    const input = ref(null);
    const buttonLabel = props.submitLabel || "Save";
    const mdText = ref(!nully(props.text) ? props.text : "");
    const pHolder = props.placeholder || "Enter text here...";
    const mdTab = ref("write");
    const disabled = computed(() => nully(mdText.value));

    const containerClasses = computed(() => {
      let clss = props.dark
        ? "md-editor-container box-arrow dark"
        : "md-editor-container box-arrow";
      return props.right ? (clss += " right") : clss;
    });

    const onUserSelected = (value) => insertText("@" + value);
    const onTicketSelected = (value) => insertText("#" + value);

    const openMarkdown = () => {
      openURL("https://docs.requarks.io/en/editors/markdown", null, {
        target: "_blank",
      });
    };

    const extendMarkdown = (md) => {
      const mention = new RegExp(/@(\w+)/, "g");
      const ticket = new RegExp(/#(\d+)/, "g");
      md.renderer.rules.text = (tokens, idx) => {
        let content = tokens[idx].content;
        if (mention.test(content)) {
          content = content.replace(
            mention,
            `<a class="mention" href="/users/$1/">$&</a>`, // eslint-disable-line
          );
        }
        if (ticket.test(content)) {
          content = content.replace(
            ticket,
            `<a class="ticket" href="/tickets/$1/">$&</a>`, // eslint-disable-line
          );
        }
        return content;
      };
    };

    const getSelection = () => {
      return [textareaEl.value.selectionStart || 0, textareaEl.value.selectionEnd];
    };

    const insertText = (text) => {
      const [start, end] = getSelection();
      mdText.value = mdText.value.slice(0, start) + `${text} ` + mdText.value.slice(end);
      input.value.focus();
    };

    const insertEnclosure = (marks) => {
      const [start, end] = getSelection();
      if (start == end || !mdText.value) {
        mdText.value = `${marks[0]}${marks[1]}`;
        textareaEl.value.focus();
        setTimeout(() => {
          textareaEl.value.setSelectionRange(marks[0].length, marks[0].length);
        }, 1);
      } else {
        const selected = mdText.value.substring(start, end);
        mdText.value =
          mdText.value.slice(0, start) +
          `${marks[0]}${selected}${marks[1]}` +
          mdText.value.slice(end);
        textareaEl.value.focus();
      }
    };

    const insertPrefix = (mark) => {
      const [start, end] = getSelection();
      if (start === end || !mdText.value) {
        mdText.value = mark === "numbered" ? "1. " : mark;
        textareaEl.value.focus();
      } else {
        let lines = mdText.value.substring(start, end).split("\n");
        lines.forEach((line, i) => {
          let lead = mark === "numbered" ? `${i + 1}. ` : mark;
          lines[i] = `${lead}${line}`;
        });
        mdText.value = mdText.value.slice(0, start) + lines.join("\n") + mdText.value.slice(end);
        textareaEl.value.focus();
      }
    };

    const onSubmit = () => {
      context.emit("onSaveText", mdText.value);
    };

    const resetEditor = () => {
      mdText.value = "";
    };

    if (props.editable) {
      onMounted(() => {
        textareaEl.value = input.value.getNativeElement();
      });
    }

    provide("onUserSelected", onUserSelected);
    provide("onTicketSelected", onTicketSelected);

    return {
      buttonLabel,
      disabled,
      extendMarkdown,
      insertEnclosure,
      insertPrefix,
      insertText,
      input,
      mdTab,
      mdText,
      onSubmit,
      openMarkdown,
      onUserSelected,
      onTicketSelected,
      pHolder,
      resetEditor,
      textareaEl,
      containerClasses,
    };
  },
});
</script>

<style lang="scss">
.md-editor-container {
  --base-colour: var(--light-bg-base-colour);
  --bg-colour: var(--light-bg-raised-colour);
  --border-colour: var(--ligth-border-base-colour);
  --text-accent: var(--light-text-accent);
  --text-detail: var(--light-secondary-text-colour);
  --toolbar-highlight: var(--light-toolbar-button-highlight);
  --textbox-bg: var(--light-textbox-bg-colour);
  --textbox-text: var(--light-textbox-colour);
  --green-button: var(--light-green-button-bg);
  --green-button-text: var(--light-green-button-text);
}
.md-editor-container.dark {
  --base-colour: var(--dark-bg-base-colour);
  --bg-colour: var(--dark-bg-raised-colour);
  --border-colour: var(--dark-border-base-colour);
  --text-accent: var(--dark-text-accent);
  --text-detail: var(--dark-secondary-text-colour);
  --toolbar-highlight: var(--dark-toolbar-button-highlight);
  --textbox-bg: var(--dark-textbox-bg-colour);
  --textbox-text: var(--dark-textbox-colour);
  --green-button: var(--dark-green-button-bg);
  --green-button-text: var(--dark-green-button-text);
}
.md-editor-container {
  min-width: 350px;
  width: 100%;
}
.md-editor-container > div:first-child {
  display: flex;
  flex-wrap: nowrap;
  padding: 4px 8px;
  background: var(--bg-colour);
}
.md-editor-container .q-tabs {
  position: relative;
  bottom: -5px;
}
.md-editor-container .q-tabs.q-tabs--dense .q-tab {
  min-height: 30px;
}
.md-editor-container .q-tabs .q-tab__label {
  font-size: 12px;
  line-height: 1.715em;
  font-weight: 500;
}
.md-editor-container .q-tabs .q-tab.q-tab--active {
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-left: 1px solid var(--border-colour);
  border-top: 1px solid var(--border-colour);
  border-right: 1px solid var(--border-colour);
  border-bottom: 1px solid var(--base-colour);
  color: var(--text-accent);
  background: var(--base-colour);
  cursor: default !important;
}
.md-editor-container .q-tabs .q-tab.q-tab--active .q-focus-helper {
  opacity: 0;
}
.md-editor-container .q-tab-panels {
  background: var(--base-colour);
}
.md-editor-container .q-tab-panels .q-field--outlined .q-field__control:before {
  border-color: var(--border-colour);
}
.md-editor-container .q-field.q-textarea .q-field__control {
  border-radius: 6px;
  padding: 0;
  background: var(--textbox-bg);
}
.md-editor-container .q-field.q-textarea .q-field__native {
  color: var(--textbox-text);
  padding: 10px;
}
.md-editor-container .md-editor-footer {
  display: flex;
  background: var(--bg-colour);
  color: var(--text-detail);
  padding: 0 8px;
  align-items: center;
  border-top: 1px solid var(--border-colour);
  height: 31px;
}
.md-editor-container .md-editor-footer .text-caption {
  height: 31px;
  overflow: hidden;
  line-height: 31px;
}
.md-editor-container .submit-button {
  background: var(--green-button);
  color: var(--green-button-text);
  font-weight: 500;
  font-size: 12px;
  padding: 0 22px;
  border-radius: 0;
  min-height: 30px;
  border-right: 1px solid var(--border-colour);
  border-left: 1px solid var(--border-colour);
}
.md-editor-container .submit-button.disabled {
  opacity: 0.2 !important;
  background: none;
  color: grey;
}
.md-editor-container .submit-button::before {
  box-shadow: none;
}
.q-markdown.dark a {
  color: var(--dark-link-colour);
}
</style>
