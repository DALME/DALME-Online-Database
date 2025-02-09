<template>
  <div class="mde-toolbar">
    <q-resize-observer @resize="setWidth" debounce="1000" />
    <q-btn icon="mdi-format-header-pound" @click="$emit('insertEnclosure', ['### ', ''])">
      <ToolTip>Add heading</ToolTip>
    </q-btn>
    <q-btn icon="mdi-format-bold" @click="$emit('insertEnclosure', ['**', '**'])">
      <ToolTip>Add bold text</ToolTip>
    </q-btn>
    <q-btn icon="mdi-format-italic" @click="$emit('insertEnclosure', ['*', '*'])">
      <ToolTip>Add italic text</ToolTip>
    </q-btn>
    <q-btn icon="mdi-format-strikethrough" @click="$emit('insertEnclosure', ['~~', '~~'])">
      <ToolTip>Add strike-through text</ToolTip>
    </q-btn>
    <q-separator vertical spaced />
    <q-btn v-if="width >= 300" icon="mdi-format-quote-close" @click="$emit('insertPrefix', '> ')">
      <ToolTip>Insert a quote</ToolTip>
    </q-btn>
    <q-btn v-if="width >= 300" icon="mdi-code-braces">
      <ToolTip>Insert code</ToolTip>
      <q-menu cover class="popup-menu" :class="dark ? 'dark' : ''">
        <q-list>
          <q-item
            dense
            v-for="(option, idx) in codeOptions"
            :key="idx"
            clickable
            v-close-popup
            @click="$emit('insertEnclosure', ['\`\`\`' + option.value + '\\n', '\\n\`\`\`'])"
          >
            <q-item-section>
              <span v-text="option.label" />
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
    <q-btn v-if="width >= 300" icon="mdi-link" @click="$emit('insertEnclosure', ['[', '](url)'])">
      <ToolTip>Insert a link</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 300"
      icon="mdi-note"
      @click="$emit('insertEnclosure', [':::\n', '\n:::'])"
    >
      <ToolTip>Insert a note</ToolTip>
    </q-btn>
    <q-separator v-if="width >= 300" vertical spaced />
    <q-btn v-if="width >= 395" icon="mdi-format-list-bulleted" @click="$emit('insertPrefix', '- ')">
      <ToolTip>Add a bulleted list</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 395"
      icon="mdi-format-list-numbered"
      @click="$emit('insertPrefix', 'numbered')"
    >
      <ToolTip>Add a numbered list</ToolTip>
    </q-btn>
    <q-btn
      v-if="width >= 395"
      icon="mdi-format-list-checks"
      @click="$emit('insertPrefix', '- [ ] ')"
    >
      <ToolTip>Add a task list</ToolTip>
    </q-btn>
    <q-separator v-if="width >= 395" vertical spaced />
    <UserChooserWidget
      v-if="width >= 420"
      :dark="dark"
      icon="mdi-account-multiple-plus"
      header="Users"
      return-field="username"
      tooltip="Mention another user"
      @item-chosen="onUserSelected"
    />
    <TicketChooserWidget
      v-if="width >= 420"
      :dark="dark"
      icon="mdi-bug"
      tooltip="Reference a ticket"
      @item-chosen="onTicketSelected"
    />

    <q-btn v-if="width < 420" icon="mdi-dots-vertical">
      <q-menu cover class="popup-menu" :class="dark ? 'dark' : ''">
        <q-list>
          <q-item
            v-if="width < 300"
            dense
            clickable
            v-close-popup
            @click="$emit('insertPrefix', '> ')"
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-quote-close" />
            </q-item-section>
            <q-item-section>Insert a quote</q-item-section>
          </q-item>

          <q-item clickable dense v-if="width < 300">
            <q-item-section avatar>
              <q-icon name="mdi-code-braces" />
            </q-item-section>
            <q-item-section>Insert code</q-item-section>
            <q-menu cover class="popup-menu" :class="dark ? 'dark' : ''">
              <q-list>
                <q-item
                  dense
                  v-for="(option, idx) in codeOptions"
                  :key="idx"
                  clickable
                  v-close-popup
                  @click="$emit('insertEnclosure', ['\`\`\`' + option.value + '\\n', '\\n\`\`\`'])"
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
            dense
            clickable
            v-close-popup
            @click="$emit('insertEnclosure', ['[', '](url)'])"
          >
            <q-item-section avatar>
              <q-icon name="mdi-link" />
            </q-item-section>
            <q-item-section>Insert a link</q-item-section>
          </q-item>

          <q-item
            v-if="width < 300"
            dense
            clickable
            v-close-popup
            @click="$emit('insertEnclosure', [':::\n', '\n:::'])"
          >
            <q-item-section avatar>
              <q-icon name="mdi-note" />
            </q-item-section>
            <q-item-section>Insert a note</q-item-section>
          </q-item>

          <q-separator spaced v-if="width < 300" />

          <q-item
            v-if="width < 395"
            dense
            clickable
            v-close-popup
            @click="$emit('insertPrefix', '- ')"
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-bulleted" />
            </q-item-section>
            <q-item-section>Add a bulleted list</q-item-section>
          </q-item>

          <q-item
            v-if="width < 395"
            dense
            clickable
            v-close-popup
            @click="$emit('insertPrefix', 'numbered')"
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-numbered" />
            </q-item-section>
            <q-item-section>Add a numbered list</q-item-section>
          </q-item>

          <q-item
            v-if="width < 395"
            dense
            clickable
            v-close-popup
            @click="$emit('insertPrefix', '- [ ] ')"
          >
            <q-item-section avatar>
              <q-icon name="mdi-format-list-checks" />
            </q-item-section>
            <q-item-section>Add a task list</q-item-section>
          </q-item>

          <q-separator spaced v-if="width < 395" />

          <UserChooserWidget
            v-if="width < 420"
            item
            :dark="dark"
            icon="mdi-account-multiple-plus"
            return-field="username"
            label="Mention another user"
            @item-chosen="onUserSelected"
          />

          <TicketChooserWidget
            v-if="width < 420"
            item
            :dark="dark"
            icon="mdi-bug"
            label="Reference a ticket"
            @item-chosen="onTicketSelected"
          />
        </q-list>
      </q-menu>
    </q-btn>
  </div>
</template>

<script>
import { defineComponent, inject, ref } from "vue";
import { UserChooserWidget, TicketChooserWidget, ToolTip } from "@/components/widgets";

export default defineComponent({
  name: "MDEToolbar",
  props: {
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  components: {
    UserChooserWidget,
    TicketChooserWidget,
    ToolTip,
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

<style lang="scss">
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
