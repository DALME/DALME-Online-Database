<template>
  <q-card :bordered="!inCard" :class="containerClasses" flat>
    <Transition enter-active-class="animated slideInDown">
      <div v-if="isEditable" class="md-editor-header">
        <q-tabs v-model="mdTab" indicator-color="transparent" dense no-caps>
          <q-tab label="Write" name="write" />
          <q-tab :disable="!mdText" label="Preview" name="preview" />
        </q-tabs>

        <MDEToolbar
          @insert-enclosure="insertEnclosure"
          @insert-prefix="insertPrefix"
          :dark="dark"
        />
      </div>
    </Transition>

    <q-tab-panels v-if="isEditable" v-model="mdTab" animated keep-alive>
      <q-tab-panel class="write-panel" name="write">
        <q-input
          ref="input"
          v-model="mdText"
          autocapitalize="off"
          autocomplete="off"
          autocorrect="off"
          type="textarea"
          dense
          outlined
        />
      </q-tab-panel>
      <q-tab-panel name="preview">
        <q-markdown
          :class="dark ? 'dark' : ''"
          :extend="extendMarkdown"
          :src="mdText"
          task-lists-enable
        />
      </q-tab-panel>
    </q-tab-panels>

    <q-markdown
      v-else
      :extend="extendMarkdown"
      :src="mdText ? mdText : placeholder"
      class="md-editor-readonly"
      task-lists-enable
    />

    <Transition enter-active-class="animated slideInUp">
      <div v-if="isEditable" class="md-editor-footer">
        <q-icon
          @click="openMarkdown"
          class="cursor-pointer q-mr-sm"
          name="mdi-language-markdown"
          size="sm"
        />
        <div v-if="help" class="text-caption">{{ help }}</div>
        <q-space />
        <q-btn
          v-if="!inCard"
          @click="onCancel"
          :disable="!hasChanged"
          class="md-button cancel text-roboto"
          label="cancel"
          dense
        />
        <q-btn
          v-if="!inCard"
          @click="onSubmit"
          :disable="!hasChanged"
          :label="submitLabel"
          class="md-button submit text-roboto"
          dense
        />
      </div>
    </Transition>
  </q-card>
</template>

<script>
import { openURL } from "quasar";
import { computed, defineComponent, inject, provide, ref, watch } from "vue";

import MDEToolbar from "./MDEToolbar.vue";

export default defineComponent({
  name: "MarkdownEditor",
  components: {
    MDEToolbar,
  },
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    right: {
      type: Boolean,
      default: false,
    },
    editable: {
      type: Boolean,
      default: false,
    },
    text: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      required: false,
      default: "Enter text here...",
    },
    help: {
      type: String,
      required: false,
      default: null,
    },
    submitLabel: {
      type: String,
      required: false,
      default: "Save",
    },
    inCard: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["onSaveText"],
  setup(props, context) {
    const input = ref(null);
    const textareaEl = computed(() => input.value.getNativeElement());
    const mdText = ref(props.text);
    const mdTab = ref("write");
    const hasChanged = computed(() => mdText.value !== props.text);
    const isEditable = props.inCard ? inject("editOn", false) : props.editable;

    const containerClasses = computed(() => {
      let clss = props.dark ? "md-editor-container dark" : "md-editor-container";
      if (props.inCard) {
        clss += " in-card";
      } else {
        clss += " box-arrow";
      }
      if (props.right) clss += " right";
      return clss;
    });

    const onUserSelected = (value) => {
      insertText("@" + value);
    };
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

    const onCancel = () => {
      mdText.value = props.text;
    };

    const resetEditor = () => {
      mdText.value = "";
    };

    provide("onUserSelected", onUserSelected);
    provide("onTicketSelected", onTicketSelected);

    if (props.inCard) {
      watch(
        () => isEditable.value,
        (val) => {
          if (val === false && hasChanged.value) {
            context.emit("onSaveText", {
              value: mdText.value,
              oldValue: props.text,
            });
          }
        },
      );
    }

    return {
      hasChanged,
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
      resetEditor,
      textareaEl,
      containerClasses,
      isEditable,
      onCancel,
    };
  },
});
</script>

<style lang="scss" scoped>
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
  --red-button: var(--light-red-button-bg);
  --red-button-text: var(--light-red-button-text);
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
  --red-button: var(--dark-red-button-bg);
  --red-button-text: var(--dark-red-button-text);
}
.md-editor-container {
  min-width: 350px;
  width: 100%;
}
.md-editor-container > .md-editor-header {
  display: flex;
  flex-wrap: nowrap;
  padding: 4px 8px;
  background: var(--bg-colour);
  border-bottom: 1px solid var(--border-colour);
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
:deep(.q-tab .q-tab__label) {
  font-size: 12px;
}
:deep(.md-editor-container .q-tabs .q-tab.q-tab--active .q-focus-helper) {
  opacity: 0;
}
.md-editor-container .q-tab-panels {
  background: var(--base-colour);
}
.md-editor-container .q-tab-panel {
  min-height: 144px;
}
.md-editor-container .write-panel {
  padding: 0 !important;
}
:deep(.write-panel .q-field--outlined .q-field__control:before) {
  border: none;
}
:deep(.write-panel .q-field--outlined .q-field__control:after) {
  border: none;
}
:deep(.write-panel .q-field--outlined .q-field__control) {
  padding: 0;
}
:deep(.write-panel .q-field.q-textarea .q-field__control) {
  background: var(--textbox-bg);
}
:deep(.write-panel .q-field.q-textarea .q-field__native) {
  color: var(--textbox-text);
  padding: 16px;
}
.md-editor-container .md-editor-footer {
  display: flex;
  background: var(--bg-colour);
  color: var(--text-detail);
  padding: 0 0 0 8px;
  align-items: center;
  border-top: 1px solid var(--border-colour);
  height: 31px;
}
.md-editor-container .md-editor-footer .text-caption {
  height: 31px;
  overflow: hidden;
  line-height: 31px;
}
.md-editor-container .md-button {
  font-weight: 500;
  font-size: 12px;
  padding: 0 22px;
  height: 100%;
  border-radius: 0;
  border-left: 1px dotted var(--border-colour);
  text-transform: capitalize;
}
.md-editor-container .md-button.submit {
  color: var(--green-button-text);
}
.md-editor-container .md-button.disabled {
  opacity: 0.2 !important;
  background: none;
  color: grey;
}
.md-editor-container .md-button::before {
  box-shadow: none;
}
.q-markdown.dark a {
  color: var(--dark-link-colour);
}
.md-editor-readonly {
  padding: 16px;
}
</style>
