<template>
  <q-card v-if="editable" flat bordered class="box-left-arrow">
    <div class="bg-grey-2 q-px-sm row justify-between items-center">
      <div class="column q-pt-xs">
        <q-tabs
          v-model="mdTab"
          dense
          shrink
          class="text-grey md-editor-tabs"
          active-color="light-blue-10"
          active-bg-color="white"
          indicator-color="transparent"
          align="left"
          narrow-indicator
          no-caps
          content-class="q-px-sm"
        >
          <q-tab name="write" label="Write" />
          <q-tab name="preview" label="Preview" :disable="disabled" />
        </q-tabs>
      </div>
      <div class="column">
        <div class="row">
          <q-btn
            color="grey-7"
            flat
            icon="text_format"
            class="md-editor-button"
            @click="insertEnclosure(['### ', ''])"
          >
            <Tooltip>Add heading</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="format_bold"
            class="md-editor-button"
            @click="insertEnclosure(['**', '**'])"
          >
            <Tooltip>Add bold text</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="format_italic"
            class="md-editor-button"
            @click="insertEnclosure(['*', '*'])"
          >
            <Tooltip>Add italic text</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="format_strikethrough"
            class="md-editor-button"
            @click="insertEnclosure(['~~', '~~'])"
          >
            <Tooltip>Add strike-through text</Tooltip>
          </q-btn>
          <q-separator vertical class="q-mr-sm" />
          <q-btn
            color="grey-7"
            flat
            icon="format_quote"
            class="md-editor-button"
            @click="insertPrefix('> ')"
          >
            <Tooltip>Insert a quote</Tooltip>
          </q-btn>
          <q-btn color="grey-7" flat icon="code" class="md-editor-button">
            <Tooltip>Insert code</Tooltip>
            <q-menu cover>
              <q-list dense>
                <q-item
                  dense
                  v-for="(option, idx) in codeOptions"
                  :key="idx"
                  clickable
                  v-close-popup
                  @click="
                    insertEnclosure([
                      '\`\`\`' + option.value + '\\n',
                      '\\n\`\`\`',
                    ])
                  "
                >
                  <q-item-section>
                    <span v-text="option.label" />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="insert_link"
            class="md-editor-button"
            @click="insertEnclosure(['[', '](url)'])"
          >
            <Tooltip>Insert a link</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="sticky_note_2"
            class="md-editor-button"
            @click="insertEnclosure([':::\n', '\n:::'])"
          >
            <Tooltip>Insert a note</Tooltip>
          </q-btn>
          <q-separator vertical class="q-mr-sm" />
          <q-btn
            color="grey-7"
            flat
            icon="format_list_bulleted"
            class="md-editor-button"
            @click="insertPrefix('- ')"
          >
            <Tooltip>Add a bulleted list</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="format_list_numbered"
            class="md-editor-button"
            @click="insertPrefix('numbered')"
          >
            <Tooltip>Add a numbered list</Tooltip>
          </q-btn>
          <q-btn
            color="grey-7"
            flat
            icon="checklist"
            class="md-editor-button"
            @click="insertPrefix('- [ ] ')"
          >
            <Tooltip>Add a task list</Tooltip>
          </q-btn>
          <q-separator vertical class="q-mr-sm" />
          <Chooser
            icon="people"
            color="grey-7"
            returnField="username"
            class="q-mr-sm"
            toolTip="Directly mention a user or team"
            target="users"
            classes="md-editor-button"
            @itemChosen="onUserSelected"
          />
          <Chooser
            icon="bug_report"
            color="grey-7"
            toolTip="Reference another issue ticket"
            target="tickets"
            classes="md-editor-button"
            @itemChosen="onTicketSelected"
          />
        </div>
      </div>
    </div>
    <q-separator />
    <q-tab-panels
      v-model="mdTab"
      keep-alive
      animated
      transition-prev="jump-up"
      transition-next="jump-up"
      class="text-body2 md-panels"
    >
      <q-tab-panel name="write" class="q-pa-sm">
        <q-input
          type="textarea"
          ref="input"
          v-model="mdText"
          outlined
          dense
          bg-color="grey-1"
          :placeholder="pHolder"
          autocapitalize="off"
          autocomplete="off"
          autocorrect="off"
          class="md-editor-textbox"
        />
        <div class="bg-grey-1 md-editor-footer q-px-sm q-py-xs items-center">
          <span v-if="help" class="text-caption text-grey-6">{{ help }}</span>
          <q-space />
          <q-icon
            name="integration_instructions"
            @click="openMarkdown"
            class="no-undeline cursor-pointer"
          >
            <Tooltip>Styling with Markdown is supported</Tooltip>
          </q-icon>
        </div>
      </q-tab-panel>
      <q-tab-panel name="preview">
        <q-markdown
          :src="mdText"
          :extend="extendMarkdown"
          style="min-height: 144px"
          task-lists-enable
        />
        <q-separator />
      </q-tab-panel>
    </q-tab-panels>
    <q-card-actions align="right" class="q-px-sm q-pt-xs md-editor-actions">
      <q-btn
        unelevated
        no-caps
        color="light-green-9"
        :disable="disabled"
        :label="buttonLabel"
        @click="onSubmit"
      />
    </q-card-actions>
  </q-card>
  <q-markdown v-else :src="mdText" :extend="extendMarkdown" task-lists-enable />
</template>

<script>
import { openURL } from "quasar";
import { isEmpty, isNil } from "ramda";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  onMounted,
  ref,
} from "vue";
import { Chooser } from "@/components/utils";

export default defineComponent({
  name: "MarkdownEditor",
  props: {
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
    Chooser,
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  emits: ["onSaveText"],
  setup(props, context) {
    const buttonLabel = props.submitLabel || "Save";
    const mdText = ref(
      !isEmpty(props.text) && !isNil(props.text) ? props.text : "",
    );
    const pHolder = props.placeholder || "Enter text here...";
    const input = ref(null);
    const mdTab = ref("write");
    const disabled = computed(() => isEmpty(mdText.value));
    const textareaEl = ref(null);
    const codeOptions = [
      { label: "CSS", value: "css" },
      { label: "HTML", value: "html" },
      { label: "JavaScript", value: "js" },
      { label: "JSON", value: "json" },
      { label: "Python", value: "py" },
      { label: "XML/TEI", value: "xml" },
    ];

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
      return [
        textareaEl.value.selectionStart || 0,
        textareaEl.value.selectionEnd,
      ];
    };

    const insertText = (text) => {
      const [start, end] = getSelection();
      mdText.value =
        mdText.value.slice(0, start) + `${text} ` + mdText.value.slice(end);
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
        mdText.value =
          mdText.value.slice(0, start) +
          lines.join("\n") +
          mdText.value.slice(end);
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

    return {
      buttonLabel,
      codeOptions,
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
    };
  },
});
</script>

<style lang="scss">
.md-editor-tabs {
  height: 29px !important;
  margin-bottom: -1px;
}
.md-editor-tabs.q-tabs--dense .q-tab {
  min-height: 30px;
}
.md-editor-tabs .q-tab__label {
  font-size: 12px;
  line-height: 1.715em;
  font-weight: 500;
}
.md-editor-tabs .q-tab.q-tab--active {
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-left: 1px solid rgb(209, 209, 209);
  border-top: 1px solid rgb(209, 209, 209);
  border-right: 1px solid rgb(209, 209, 209);
  border-bottom: 1px solid white;
}
.md-panels .q-field--outlined .q-field__control:before {
  border-color: rgb(209, 209, 209);
  border-bottom-style: dashed;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.md-editor-footer {
  display: flex;
  border-top: none;
  border-left: 1px solid rgb(209, 209, 209);
  border-right: 1px solid rgb(209, 209, 209);
  border-bottom: 1px solid rgb(209, 209, 209);
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
.md-editor-textbox .q-field__control {
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 0px;
}
.md-editor-button {
  font-size: 11px;
  padding: 4px;
  margin-right: 2px;
}
.md-editor-button:last-of-type {
  margin-right: 0;
}
</style>
