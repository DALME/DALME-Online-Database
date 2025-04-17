<template>
  <div v-show="!rendering" ref="rendered-tei" class="transcription" />
  <AdaptiveSpinner v-show="rendering" type="hourglass" adaptive color="grey-5" size="10%" />
</template>

<script>
import { computed, defineComponent, nextTick, ref, watch, useTemplateRef } from "vue";
import { useConstants, useStores } from "@/use";
import CETEI from "CETEIcean";
import { idaTeiBehaviours } from "./behaviours.js";
import { createPopper } from "@popperjs/core";
import { AdaptiveSpinner } from "@/components";

export default defineComponent({
  name: "TeiRenderer",
  props: {
    text: {
      type: String,
      required: false,
      default: null,
    },
  },
  components: { AdaptiveSpinner },
  setup(props) {
    const { currentPageData } = useStores();
    const { teiSelectors } = useConstants();
    const teiContainer = useTemplateRef("rendered-tei");
    const hasBraces = ref(false);
    const hasMarginalNotes = ref(false);
    const hasRenvois = ref(false);
    const hasColumns = ref(false);
    const hasLeaders = ref(false);
    const teiRenderer = new CETEI();
    const rendering = ref(false);
    const tooltipInstances = ref([]);

    teiRenderer.addBehaviors(idaTeiBehaviours);

    const teiDoc = computed(() => {
      const transcription = props.text
        ? props.text
        : currentPageData.value.tei
          ? currentPageData.value.tei
          : "";
      return `<TEI xmlns="http://www.tei-c.org/ns/1.0">\
                  <text>\
                    <body>${transcription.replace(/\n/g, "<lb/>")}</body>\
                  </text>\
                </TEI>`;
    });

    const generateTei = () => {
      rendering.value = true;
      teiRenderer.makeHTML5(teiDoc.value, processTei, addSpans);
    };

    const addSpans = (newElement) => {
      for (let node of Array.from(newElement.childNodes)) {
        if (node.nodeType !== Node.ELEMENT_NODE) {
          if (node.cloneNode().textContent.trim()) {
            let span = document.createElement("SPAN");
            span.innerText = node.textContent;
            node.replaceWith(span);
          }
        }
      }
    };

    const processTei = (html) => {
      return new Promise((resolve) => {
        hasBraces.value = Boolean(html.querySelectorAll(teiSelectors.braces).length);
        hasMarginalNotes.value = Boolean(html.querySelectorAll(teiSelectors.marginalNotes).length);
        hasRenvois.value = Boolean(html.querySelectorAll(teiSelectors.renvois).length);
        hasColumns.value = Boolean(html.querySelectorAll(teiSelectors.columns).length);
        hasLeaders.value = Boolean(html.querySelectorAll(teiSelectors.leaders).length);
        applyFixes(html).then((result) => {
          teiContainer.value.innerHTML = "";
          teiContainer.value.append(result);
          nextTick().then(() => {
            applyTooltips();
            rendering.value = false;
            resolve();
          });
        });
      });
    };

    const applyFixes = (html) => {
      return new Promise((resolve) => {
        // set up braces -> move notes inside seg tag
        if (hasBraces.value) {
          html.querySelectorAll(teiSelectors.braces).forEach((el) => {
            let target = el.getAttribute("target");
            if (target) {
              if (target.length > 1 && target.startsWith("#")) {
                target = target.substring(1);
              }
              el.append(html.querySelector(`tei-note#${target}`));
            }
          });
        }
        // set up marginal notes
        if (hasMarginalNotes.value) {
          let notesContainer = html.querySelector(".notes_container");
          html.querySelectorAll(teiSelectors.marginalNotes).forEach((el) => {
            el.style.top = `${Math.round(el.getBoundingClientRect().top)}px`;
            notesContainer.append(el);
          });
          notesContainer.style.height = `${html.querySelector("tei-text").offsetHeight}px`;
          // $('#transcription').on('scroll', function (e) {
          //   $('#notebar').scrollTop($(this).scrollTop());
          // });
          // $('#notebar').on('scroll wheel', function(e) {
          //   e.preventDefault();
          //   e.stopPropagation();
          //   return false;
          // });
        }
        // set up columns
        if (hasColumns.value) {
          html.addEventListener("click", (evt) => {
            if (evt.target.classList.contains(".ab-column-toggler")) {
              const parent = evt.target.closest("tei-ab");
              parent.classList.toggle("closed");
            }
          });
        }
        /* eslint-disable */
        // set up marginal leaders
        // if (hasLeaders.value) {
        //   html.querySelectorAll(teiSelectors.leaders).forEach((el) => {
        // let sum = 0;
        // let prev_array = [];
        // let next_array = [];
        // let prevSibs = prevUntil(el, "tei-lb");
        // let prevChild = prevUntil(el, "*:has(tei-lb)");
        // let nextSibs = nextUntil(el, "tei-lb");
        // let nextChild = nextUntil(el, "*:has(tei-lb)");
        // if (prevChild.length < prevSibs.length) {
        //   let prev_el = prevChild.length ? prevChild : el;
        //   prev_array = $.merge(prevChild, $(prev_el).prev().children().nextUntil('tei-lb'));
        // } else {
        //   prev_array = prevSibs;
        // }
        // if (nextChild.length < nextSibs.length) {
        //   let next_el = nextChild.length ? nextChild : this;
        //   next_array = $.merge(nextChild, $(next_el).next().children().nextUntil('tei-lb'));
        // } else {
        //   next_array = nextSibs;
        // }
        // const line_el = $.merge(prev_array, next_array)
        // line_el.each(function(i, elt) { sum += $(this).innerWidth(); });
        // const container_column = $(this).parents('.ab-content');
        // if (container_column.length) {
        //   let column_width = container_column.attr('width');
        //   if (typeof column_width === typeof undefined || column_width === false) {
        //     container_column.attr('width', container_column.innerWidth());
        //   }
        //   container_width = container_column.attr('width');
        // }
        // let target_width = container_width - sum - 15;
        // target_width = target_width > 10 ? target_width : 10;
        // $(this).width(target_width);
        // });
        // }
        /* eslint-enable */
        // set up renvois
        if (hasRenvois.value) {
          html.querySelectorAll(teiSelectors.renvois).forEach((el) => {
            let noteId = el.getAttribute("target");
            if (noteId.length > 1 && noteId.startsWith("#")) {
              noteId = noteId.substring(1);
            }
            let note = html.querySelector(`tei-note#${noteId}`);
            if (note.length) {
              el.setAttribute("title", note.innerHTML);
              el.setAttribute("data-toggle", "tooltip");
              el.setAttribute("data-html", true);
              el.setAttribute(
                "data-template",
                '<div class="tooltip note" role="tooltip"><div class="arrow">\
                </div><div class="tooltip-inner"></div></div>',
              );
            }
          });
        }
        resolve(html);
      });
    };

    const showTooltip = (evt) => {
      const tooltip = evt.target.querySelector("div.tei-tooltip");
      const popinstance = tooltipInstances.value[parseInt(tooltip.id.slice(8))];
      tooltip.setAttribute("data-show", "");
      popinstance.update();
    };

    const hideTooltip = (evt) => {
      const tooltip = evt.target.querySelector("div.tei-tooltip");
      tooltip.removeAttribute("data-show");
    };

    const applyTooltips = () => {
      document.querySelectorAll('[data-toggle="tooltip"]').forEach((el, idx) => {
        tooltipInstances.value.push(
          createPopper(el.parentNode, el, { scroll: true, resize: true }),
        );
        el.id = `tooltip-${idx}`;
        el.classList.add("tei-tooltip-arrow");
        el.parentNode.addEventListener("mouseenter", showTooltip);
        el.parentNode.addEventListener("mouseleave", hideTooltip);
      });
    };

    // const dir = (elem, dir, until) => {
    //   let matched = [];
    //   let cur = elem[dir];
    //   while (
    //     cur &&
    //     cur.nodeType !== 9 &&
    //     (until === undefined ||
    //       cur.nodeType !== 1 ||
    //       !cur.matchesSelector(until))
    //   ) {
    //     if (cur.nodeType === 1) {
    //       matched.push(cur);
    //     }
    //     cur = cur[dir];
    //   }
    //   return matched;
    // };

    // const prevUntil = (elem, until) => {
    //   return dir(elem, "previousSibling", until);
    // };
    //
    // const nextUntil = (elem, until) => {
    //   return dir(elem, "nextSibling", until);
    // };

    // toggleTeiContainers() {
    //   const containerList = [
    //     { selector: 'tei-ab[type=column] div.ab-content', parent: true },
    //     { selector: 'tei-layout[columns]', parent: false },
    //     { selector: 'tei-note:not([type])', parent: false }
    //   ];
    //   const that = this;
    //   for (let i = 0, len = containerList.length; i < len; ++i) {
    //     $(containerList[i].selector).each(function() {
    //       const target = containerList[i].parent ? $(this).parent() : $(this);
    //       const all_children = $(this).children(':not(tei-lb)');
    //       const hidden_children = $(this).children(':not(tei-lb)').filter(function() {
    //         return $(this).css('display') == 'none';
    //       });
    //       all_children.length === hidden_children.length ? target.hide() : target.show();
    //     });
    //   }
    // },

    // updateTeiRendering(e) {
    //   if (this.hasLeaders) {
    //     this.formatLeaders();
    //   }
    //   if (this.hasMarginalNotes) {
    //     let prev_height = $('.notes_container').height();
    //     $('.notes_container').height(e.height);
    //     $('tei-note[type=marginal]').each(function() {
    //       let new_top = (parseInt($(this).css('top'), 10) / prev_height) * e.height;
    //       $(this).css({ top: `${Math.round(new_top)}px`});
    //     });
    //   }
    // },

    watch(
      () => currentPageData.value.tei,
      () => generateTei(),
      { immediate: true },
    );

    return {
      rendering,
    };
  },
});
</script>

<style>
@import "./tei.css";
.transcription {
  position: relative;
  width: 100%;
  padding: 30px;
  display: flex;
}
.tei-tooltip {
  background: #333;
  color: white;
  font-weight: bold;
  padding: 4px 8px;
  font-size: 13px;
  border-radius: 4px;
  display: none;
}
.tei-tooltip[data-show] {
  display: block;
}
.tei-tooltip-arrow::after {
  content: "";
  position: absolute;
  border-width: 8px;
  border-style: solid;
  border-top-color: transparent;
  border-right-color: transparent;
  border-bottom-color: transparent;
  border-left-color: transparent;
}
.tei-tooltip-arrow[data-popper-placement^="top"]::after {
  left: calc(50% - 8px);
  border-top-color: #333;
  top: 100%;
}
.tei-tooltip-arrow[data-popper-placement^="left"]::after {
  top: calc(50% - 8px);
  border-left-color: #333;
  left: 100%;
}
.tei-tooltip-arrow[data-popper-placement^="right"]::after {
  top: calc(50% - 8px);
  border-right-color: #333;
  right: 100%;
}
.tei-tooltip-arrow[data-popper-placement^="bottom"]::after {
  left: calc(50% - 8px);
  bottom: 100%;
  border-bottom-color: #333;
}
</style>
