<template v-for="el in dom">
  <component :is="el.tag">
    <template v-for="child in el.children">
      <template v-if="child.type === 3">
        ${child.text}
      </template>
      <template v-else>
        <component :is="el.tag">
        </component>
      </template>
    </template>
  </component>
</template>

<script>
export default {
  name: 'DALME TEI Renderer',
  props: {
    xmlData: String,
  },
  mounted() {
    this.parseDom();
  },
  data: function () {
    return {
      // namespaces: new Map(),
      // els: null,
      dom: null,
      // elementList: [],
    }
  },
  computed: {
    xmlAsDom(this.xmlData) {
      return (new DOMParser()).parseFromString(xmlData, "text/xml");
    },
  },
  methods: {
    // learnElementNames() {
    //   const root = this.xmlAsDom.documentElement;
    //   let i = 1;
    //   const els = new Set( Array.from(root.querySelectorAll("*")) );
    //   return els
    // },
    parseDom() {
      // this.els = this.learnElementNames(this.xmlAsDom);
      this.dom = getParsedEl(this.xmlAsDom.documentElement);
      // this.applyBehaviors();
      // this.done = true;
      // return this.dom;
    },
    getParsedEl(el) {
      let newElement = {
        tag: el.localName,
        type: el.nodeType,
        attributes: {},
        children: []
      };
      // Copy attributes; @xmlns, @xml:id, @xml:lang, and
      // @rendition get special handling.
      for (let att of Array.from(el.attributes)) {
          if (att.name == "xmlns") {
            //Strip default namespaces, but hang on to the values
            newElement.attributes["data-xmlns"] = att.value;
          } else {
            newElement.attributes[att.name] = att.value;
          }
          if (att.name == "xml:id") {
            newElement.attributes["id"] = att.value;
          }
          if (att.name == "xml:lang") {
            newElement.attributes["lang"] = att.value;
          }
          if (att.name == "rendition") {
            newElement.attributes["class"] = att.value.replace(/#/g, ""));
          }
      }
      // Preserve element name so we can use it later
      newElement.attributes["data-origname"] = el.localName;
      if (el.hasAttributes()) {
        newElement.attributes["data-origatts"] = el.getAttributeNames().join(" "));
      }
      // If element is empty, flag it
      if (el.childNodes.length == 0) {
        newElement.attributes["data-empty"] = "";
      }
      for (let node of Array.from(el.childNodes)) {
          if (node.nodeType == Node.ELEMENT_NODE) {
              newElement.attributes["children"].push(this.getParsedEl(node));
          }
          else {
              newElement.attributes["children"].push({
                type: node.nodeType,
                text: node.nodeValue,
              });
          }
      }
      return newElement;
    }
  }
}
</script>
