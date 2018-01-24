/**
 * Look up a term in the Getty AAT thesaurus, display the results in an element
 * identified by displayId with the template identified by templateId
 * @param {string} term - The term to look up in the Getty AAT thesaurus
 * @param {string} templateId - The ID of the handlebars template to use
 * @param {string} displayId - The ID of the element which will contain the
 * results of the query, styled by the template.
 */
function gettySearch(term,templateId,displayId) {
  // Set up ID variables
  if (templateId.startsWith('#') == false) {
    templateId = '#'+templateId;
  }
  if (displayId.startsWith('#') == false) {
    displayId = '#'+displayId;
  }
  // Set up query string and urls
  var query = "select ?Subject ?Term ?Parents ?ScopeNote {\
                ?Subject a skos:Concept; luc:term\"" + term + "\"; skos:inScheme aat: ;\
                    gvp:prefLabelGVP [xl:literalForm ?Term].\
                optional {?Subject gvp:parentStringAbbrev ?Parents}\
                optional {?Subject skos:scopeNote [dct:language gvp_lang:en; rdf:value ?ScopeNote]}\
              } order by asc(lcase(str(?Term)))";
  var jsonQueryUrl = "http://vocab.getty.edu/sparql.json?query=" + query + "&toc=Case-insensitive_Full_Text_Search_Query&implicit=true&equivalent=false&_form=/queriesF";
  var htmlQueryUrl = "http://vocab.getty.edu/sparql?query=" + query + "&toc=Case-insensitive_Full_Text_Search_Query&implicit=true&equivalent=false&_form=/queriesF";
  // Set up display objects
  var displayContainer = $(displayId);
  var source = $(templateId).html();
  var template = Handlebars.compile(source);
  $.getJSON(jsonQueryUrl, function( data ) {
    displayContainer.empty();
    displayContainer.append("<a href='" + htmlQueryUrl + "'>View search on Getty site</a>");
    if (data['results']['bindings'].length == 0) {
      displayContainer.append("<p>No results for \"" + term + "\"");
    } else {
      $.each( data['results']['bindings'], function( i, result ) {
        var context = {};
        context['subject'] = result['Subject']['value'];
        context['term']    = result['Term']['value'];
        if ('ScopeNote' in result) {
          context['scopeNote'] = result['ScopeNote']['value'];
        }
        if ('Parents' in result) {
          context['parents'] = result['Parents']['value'];
        }
        var entry = template(context);
        displayContainer.append(entry);
      });
    }
  });
}
