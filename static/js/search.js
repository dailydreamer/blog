var lunrIndex, pagesIndex;

// Initialize lunrjs using our generated index file
function initLunr() {
  // First retrieve the index file
  $.getJSON("/index.json", function (index) {
    pagesIndex = index;
    // Set up lunrjs by declaring the fields we use
    // Also provide their boost level for the ranking
    lunrIndex = lunr(function () {
      this.ref('uri')
      this.field('title', {
        boost: 15
      });
      this.field('tags', {
        boost: 10
      });
      this.field("content", {
        boost: 5
      });

      pagesIndex.forEach(function (doc) {
        this.add(doc)
      }, this)
    })
    // lunrIndex.pipeline.remove(lunrIndex.stemmer)
  })
}

/**
 * Trigger a search in lunr and transform the result
 *
 * @param  {String} query
 * @return {Array}  results
 */
function search(query) {
  // Find the item in our index corresponding to the lunr one to have more info
  return lunrIndex.search(query).map(function (result) {
    return pagesIndex.filter(function (page) {
      return page.uri === result.ref;
    })[0];
  });
}

// Let's get started
initLunr();

$(document).ready(function () {
  var horseyList = horsey($("#search-by").get(0), {
    suggestions: function (value, done) {
      var query = $("#search-by").val();
      var results = search(query);
      done(results);
    },
    filter: function (q, suggestion) {
      return true;
    },
    set: function (value) {
      location.href = value.uri;
    },
    render: function (li, suggestion) {
      var uri = suggestion.uri.substring(1, suggestion.uri.length);

      suggestion.href = uri;

      var query = $("#search-by").val();
      var numWords = 2;
      var text = suggestion.content.match("(?:\\s?(?:[\\w]+)\\s?){0," + numWords + "}" + query + "(?:\\s?(?:[\\w]+)\\s?){0," + numWords + "}");
      suggestion.context = text;
      var image = '<div>' + '» ' + suggestion.title + '</div><div style="font-size:12px">' + (suggestion.context || '') + '</div>';
      li.innerHTML = image;
    },
    limit: 10
  });
  horseyList.refreshPosition();
});