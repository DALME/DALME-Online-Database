<template>
  <q-card v-if="editable" flat bordered class="box-left-arrow">
    <q-card-section class="bg-grey-2 q-py-xs q-px-sm row">
      <q-space />
      <div class="row">
        <q-btn
          color="grey-7"
          flat
          icon="text_format"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure(['### ', ''])"
        >
          <Tooltip>Add heading</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="format_bold"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure(['**', '**'])"
        >
          <Tooltip>Add bold text</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="format_italic"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure(['*', '*'])"
        >
          <Tooltip>Add italic text</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="format_strikethrough"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure(['~~', '~~'])"
        >
          <Tooltip>Add strike-through text</Tooltip>
        </q-btn>
        <q-separator vertical class="q-mr-sm" />
        <q-btn
          color="grey-7"
          flat
          icon="format_quote"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertPrefix('> ')"
        >
          <Tooltip>Insert a quote</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="code"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
        >
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
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure(['[', '](url)'])"
        >
          <Tooltip>Insert a link</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="sticky_note_2"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertEnclosure([':::\n', '\n:::'])"
        >
          <Tooltip>Insert a note</Tooltip>
        </q-btn>
        <q-separator vertical class="q-mr-sm" />
        <q-btn
          color="grey-7"
          flat
          icon="format_list_bulleted"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertPrefix('- ')"
        >
          <Tooltip>Add a bulleted list</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="format_list_numbered"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertPrefix('numbered')"
        >
          <Tooltip>Add a numbered list</Tooltip>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="checklist"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
          @click="insertPrefix('- [ ] ')"
        >
          <Tooltip>Add a task list</Tooltip>
        </q-btn>
        <q-separator vertical class="q-mr-sm" />
        <q-btn
          color="grey-7"
          flat
          icon="people"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
        >
          <Tooltip>Directly mention a user or team</Tooltip>
          <q-menu anchor="top left" self="top left">
            <q-input
              dense
              square
              filled
              hide-bottom-space
              v-model="filterUsers"
              debounce="300"
              autocomplete="off"
              autocorrect="off"
              autocapitalize="off"
              spellcheck="false"
              label="Filter"
            >
              <template v-slot:append>
                <q-icon
                  v-if="filterUsers === ''"
                  name="search"
                  color="blue-grey-7"
                  size="xs"
                />
                <q-icon
                  v-else
                  name="highlight_off"
                  class="cursor-pointer"
                  color="blue-grey-7"
                  size="xs"
                  @click="filterUsers = ''"
                />
              </template>
            </q-input>
            <q-list>
              <template v-for="(entry, idx) in users" :key="idx">
                <q-item
                  dense
                  clickable
                  v-close-popup
                  @click="insertText('@' + entry.username)"
                >
                  <q-item-section>
                    <div class="row items-center">
                      <span
                        class="text-weight-medium q-mr-sm"
                        v-text="entry.username"
                      />
                      <span
                        class="text-caption text-grey-6"
                        v-text="entry.fullName"
                      />
                    </div>
                  </q-item-section>
                </q-item>
                <q-separator />
              </template>
            </q-list>
          </q-menu>
        </q-btn>
        <q-btn
          color="grey-7"
          flat
          icon="bug_report"
          size="12px"
          padding="5px 5px"
          class="q-mr-sm"
        >
          <Tooltip>Reference another issue ticket</Tooltip>
          <q-menu anchor="top left" self="top left">
            <q-input
              dense
              square
              filled
              hide-bottom-space
              v-model="filterTickets"
              debounce="300"
              autocomplete="off"
              autocorrect="off"
              autocapitalize="off"
              spellcheck="false"
              label="Filter"
            >
              <template v-slot:append>
                <q-icon
                  v-if="filterTickets === ''"
                  name="search"
                  color="blue-grey-7"
                  size="xs"
                />
                <q-icon
                  v-else
                  name="highlight_off"
                  class="cursor-pointer"
                  color="blue-grey-7"
                  size="xs"
                  @click="filterTickets = ''"
                />
              </template>
            </q-input>
            <q-list>
              <template v-for="(entry, idx) in tickets" :key="idx">
                <q-item
                  dense
                  clickable
                  v-close-popup
                  @click="insertText('#' + entry.id)"
                >
                  <q-item-section>
                    <div class="row items-center">
                      <q-icon
                        :name="
                          entry.status == 0
                            ? 'fas fa-exclamation-circle'
                            : 'fas fa-check-circle'
                        "
                        :color="entry.status == 0 ? 'green-8' : 'red-8'"
                        class="q-mr-sm"
                      />
                      <span
                        class="text-grey-6 q-mr-sm"
                        v-text="'#' + entry.id"
                      />
                      <span
                        class="text-grey-8 text-weight-bold q-mr-sm"
                        v-text="entry.subject"
                      />
                    </div>
                  </q-item-section>
                </q-item>
                <q-separator />
              </template>
            </q-list>
          </q-menu>
        </q-btn>
      </div>
    </q-card-section>
    <q-separator />
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
      style="max-width: 180px"
    >
      <q-tab name="write" label="Write" />
      <q-tab name="preview" label="Preview" :disable="disabled" />
    </q-tabs>
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
import { filter, isEmpty, isNil } from "ramda";
import {
  computed,
  defineAsyncComponent,
  defineComponent,
  onMounted,
  ref,
} from "vue";
import { requests } from "@/api";
import { useAPI, useNotifier } from "@/use";
import { ticketListSchema, userSelectSchema } from "@/schemas";

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
    Tooltip: defineAsyncComponent(() =>
      import("@/components/utils/Tooltip.vue"),
    ),
  },
  emits: ["onSaveText"],
  setup(props, context) {
    const { apiInterface } = useAPI();
    const { data, fetchAPI, success } = apiInterface();
    const $notifier = useNotifier();
    const buttonLabel = props.submitLabel || "Save";
    const mdText = ref(
      !isEmpty(props.text) && !isNil(props.text) ? props.text : "",
    );
    const pHolder = props.placeholder || "Enter text here...";
    const input = ref(null);
    const mdTab = ref("write");
    const disabled = computed(() => isEmpty(mdText.value));
    const userList = ref([]);
    const ticketList = ref([]);
    const textareaEl = ref(null);
    const filterUsers = ref("");
    const filterTickets = ref("");
    const codeOptions = [
      { label: "CSS", value: "css" },
      { label: "HTML", value: "html" },
      { label: "JavaScript", value: "js" },
      { label: "JSON", value: "json" },
      { label: "Python", value: "py" },
      { label: "XML/TEI", value: "xml" },
    ];

    const users = computed(() => {
      if (isEmpty(filterUsers.value)) {
        return userList.value;
      } else {
        return filter(
          (user) =>
            user.username.includes(filterUsers.value) ||
            user.fullName.includes(filterUsers.value),
          userList.value,
        );
      }
    });

    const tickets = computed(() => {
      if (isEmpty(filterTickets.value)) {
        return ticketList.value;
      } else {
        return filter(
          (ticket) =>
            ticket.creationUser.fullName.includes(filterTickets.value) ||
            ticket.creationUser.username.includes(filterTickets.value) ||
            ticket.description.includes(filterTickets.value) ||
            ticket.subject.includes(filterTickets.value),
          ticketList.value,
        );
      }
    });

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

    const getUserList = async () => {
      await fetchAPI(requests.users.getUsers());
      if (success.value) {
        await userSelectSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            userList.value = value;
          });
      } else {
        $notifier.users.userListRetrievalFailed();
      }
    };

    const getTicketList = async () => {
      await fetchAPI(requests.tickets.getTickets());
      if (success.value) {
        ticketList.value = data.value;
        await ticketListSchema
          .validate(data.value, { stripUnknown: true })
          .then((value) => {
            ticketList.value = value;
          });
      } else {
        $notifier.tickets.ticketListRetrievalFailed();
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
        getUserList();
        getTicketList();
      });
    }

    return {
      buttonLabel,
      codeOptions,
      disabled,
      extendMarkdown,
      filterUsers,
      filterTickets,
      getUserList,
      getTicketList,
      insertEnclosure,
      insertPrefix,
      insertText,
      input,
      mdTab,
      mdText,
      onSubmit,
      openMarkdown,
      pHolder,
      resetEditor,
      textareaEl,
      tickets,
      users,
    };
  },
});
</script>

<style lang="scss" scoped>
.md-editor-tabs {
  max-width: 180px;
  margin-top: -36px;
}
.md-editor-tabs .q-tab.q-tab--active {
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-left: 1px solid #e0e0e0;
  border-top: 1px solid #e0e0e0;
  border-right: 1px solid #e0e0e0;
  border-bottom: 1px solid white;
  margin-bottom: -1px;
}
.md-panels .q-field--outlined .q-field__control:before {
  border-color: #e0e0e0;
  border-bottom: none;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.md-editor-footer {
  display: flex;
  border-top: none;
  border-left: 1px solid rgba(0, 0, 0, 0.24);
  border-right: 1px solid rgba(0, 0, 0, 0.24);
  border-bottom: 1px solid rgba(0, 0, 0, 0.24);
  border-top-left-radius: 0px;
  border-top-right-radius: 0px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
}
</style>
