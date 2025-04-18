<template>
  <div class="mde-toolbar">
    <q-resize-observer @resize="setWidth" debounce="1000" />
    <q-btn @click="$emit('insertEnclosure', ['### ', ''])" icon="mdi-format-header-pound">
      <ToolTip>Add heading</ToolTip>
    </q-btn>
    <q-btn @click="$emit('insertEnclosure', ['**', '**'])" icon="mdi-format-bold">
      <ToolTip>Add bold text</ToolTip>
    </q-btn>
    <q-btn @click="$emit('insertEnclosure', ['*', '*'])" icon="mdi-format-italic">
      <ToolTip>Add italic text</ToolTip>
    </q-btn>
    <q-btn @click="$emit('insertEnclosure', ['~~', '~~'])" icon="mdi-format-strikethrough">
      <ToolTip>Add strike-through text</ToolTip>
    </q-btn>
    <q-separator spaced vertical />
    <q-btn v-if="width >= 300" @click="$emit('insertPrefix', '> ')" icon="mdi-format-quote-close">
      <ToolTip>Insert a quote</ToolTip>
    </q-btn>
    <q-btn v-if="width >= 300" icon="mdi-code-braces">
      <ToolTip>Insert code</ToolTip>
      <q-menu :class="dark ? 'dark' : ''" class="popup-menu" cover>
        <q-list>
          <q-item
            v-for="(option, idx) in codeOptions"
            :key="idx"
            v-close-popup
            @click="$emit('insertEnclosure', ['\`\`\`' + option.value + '\\n', '\\n\`\`\`'])"
            clickable
            dense
          >
            <q-item-section>
              <span v-text="option.label" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
    <q-btn v-if="width >= 300" @click="$emit('insertEnclosure', ['[', '](url)'])" icon="mdi-link">
      <ToolTip>Insert a link</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 300"
      @click="$emit('insertEnclosure', [':::\n', '\n:::'])"
      icon="mdi-note"
    >
      <ToolTip>Insert a note</ToolTip>
    </q-btn>
    <q-separator v-if="width >= 300" spaced vertical />
    <q-btn v-if="width >= 395" @click="$emit('insertPrefix', '- ')" icon="mdi-format-list-bulleted">
      <ToolTip>Add a bulleted list</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 395"
      @click="$emit('insertPrefix', 'numbered')"
      icon="mdi-format-list-numbered"
    >
      <ToolTip>Add a numbered list</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 395"
      @click="$emit('insertPrefix', '- [ ] ')"
      icon="mdi-format-list-checks"
    >
      <ToolTip>Add a task list</ToolTip>
    </q-btn>
    <q-separator v-if="width >= 395" spaced vertical />
    <GeneralChooser
      v-if="width >= 420"
      @item-chosen="onUserSelected"
      :dark="dark"
      :toggle="false"
      icon="mdi-account-multiple-plus"
      return-field="username"
      tooltip="Mention another user"
      type="users"
    />
    <GeneralChooser
      v-if="width >= 420"
      @item-chosen="onTicketSelected"
      :dark="dark"
      :toggle="false"
      icon="mdi-bug"
      return-field="number"
      tooltip="Reference a ticket"
      type="tickets"
    />

    <q-btn v-if="width < 420" icon="mdi-dots-vertical">
      <q-menu :class="dark ? 'dark' : ''" class="popup-menu" cover>
        <q-list>
          <q-item
            v-if="width < 300"
            v-close-popup
            @click="$emit('insertPrefix', '> ')"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-quote-close" />
            </q-item-section>
            <q-item-section>Insert a quote</q-item-section>
          </q-item>

          <q-item v-if="width < 300" clickable dense>
            <q-item-section avatar>
              <q-icon name="mdi-code-braces" />
            </q-item-section>
            <q-item-section>Insert code</q-item-section>
            <q-menu :class="dark ? 'dark' : ''" class="popup-menu" cover>
              <q-list>
                <q-item
                  v-for="(option, idx) in codeOptions"
                  :key="idx"
                  v-close-popup
                  @click="$emit('insertEnclosure', ['\`\`\`' + option.value + '\\n', '\\n\`\`\`'])"
                  clickable
                  dense
                >
                  <q-item-section>
                    <span v-text="option.label" />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-item>

          <q-item
            v-if="width < 300"
            v-close-popup
            @click="$emit('insertEnclosure', ['[', '](url)'])"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-link" />
            </q-item-section>
            <q-item-section>Insert a link</q-item-section>
          </q-item>

          <q-item
            v-if="width < 300"
            v-close-popup
            @click="$emit('insertEnclosure', [':::\n', '\n:::'])"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-note" />
            </q-item-section>
            <q-item-section>Insert a note</q-item-section>
          </q-item>

          <q-separator v-if="width < 300" spaced />

          <q-item
            v-if="width < 395"
            v-close-popup
            @click="$emit('insertPrefix', '- ')"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-bulleted" />
            </q-item-section>
            <q-item-section>Add a bulleted list</q-item-section>
          </q-item>

          <q-item
            v-if="width < 395"
            v-close-popup
            @click="$emit('insertPrefix', 'numbered')"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-numbered" />
            </q-item-section>
            <q-item-section>Add a numbered list</q-item-section>
          </q-item>

          <q-item
            v-if="width < 395"
            v-close-popup
            @click="$emit('insertPrefix', '- [ ] ')"
            clickable
            dense
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-checks" />
            </q-item-section>
            <q-item-section>Add a task list</q-item-section>
          </q-item>

          <q-separator v-if="width < 395" spaced />

          <GeneralChooser
            v-if="width < 420"
            @item-chosen="onUserSelected"
            :dark="dark"
            icon="mdi-account-multiple-plus"
            label="Mention another user"
            return-field="username"
            type="users"
            item
          />

          <GeneralChooser
            v-if="width < 420"
            @item-chosen="onTicketSelected"
            :dark="dark"
            icon="mdi-bug"
            label="Reference a ticket"
            return-field="number"
            type="tickets"
            item
          />
        </q-list>
      </q-menu>
    </q-btn>
  </div>
</template>

<script>
import { defineComponent, inject, ref } from "vue";

import { GeneralChooser, ToolTip } from "@/components/widgets";

export default defineComponent({
  name: "MDEToolbar",
  components: {
    GeneralChooser,
    ToolTip,
  },
  props: {
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  emits: ["insertEnclosure", "insertPrefix"],
  setup() {
    const onUserSelected = inject("onUserSelected");
    const onTicketSelected = inject("onTicketSelected");
    const width = ref(0);
    const codeOptions = [
      { label: "CSS", value: "css" },
      { label: "HTML", value: "html" },
      { label: "JavaScript", value: "js" },
      { label: "JSON", value: "json" },
      { label: "Python", value: "py" },
      { label: "XML/TEI", value: "xml" },
    ];

    const setWidth = (size) => {
      width.value = size.width;
    };

    return {
      width,
      codeOptions,
      setWidth,
      onUserSelected,
      onTicketSelected,
    };
  },
});
</script>

<style lang="scss" scoped>
.md-editor-container .mde-toolbar {
  display: flex;
  flex-grow: 1;
  justify-content: flex-end;
  min-width: 155px;
  flex-wrap: nowrap;
}
.md-editor-container .mde-toolbar .q-btn {
  color: var(--text-detail);
  font-size: 11px;
  padding: 0;
  width: 28px;
}
.md-editor-container .mde-toolbar .q-btn::before {
  box-shadow: none;
}
.md-editor-container .mde-toolbar .q-btn:hover > .q-focus-helper {
  opacity: 0;
}
.md-editor-container .mde-toolbar .q-btn:hover {
  color: var(--toolbar-highlight);
}
.md-editor-container .mde-toolbar .q-separator {
  height: 28px;
  align-self: center;
}
</style>
