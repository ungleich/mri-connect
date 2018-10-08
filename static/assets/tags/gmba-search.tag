<gmba-search>

  <form onsubmit={ search }>
    <div class="o-field o-field--icon-left">
      <i class="material-icons">
        search
      </i>
      <button onclick={ resetsearch } type="button" class="c-button c-button--close" title="Reset search">&times;</button>
      <input name="query" class="c-field" placeholder="Search ..." type="text" />
    </div>
  </form>

  <form class="field-filters" onsubmit={ search } autocomplete="off">
    <div class="o-grid o-grid--wrap o-grid--small-full o-grid--medium-small o-grid--large-full">

      <div class="o-grid__cell o-grid__cell--width-25">

        <i class="material-icons">
        public
        </i>
        <input name="filter-country" type="text" class="c-field" placeholder="Country" onfocus={ focusfilter } onkeydown={ focusfilter } />

        <div role="menu" class="c-card c-card--menu u-high">
          <label role="menuitem" class="c-card__control c-field c-field--choice"
            each={ f in filters_shown.country }
            data-target="filter-country" onclick={ selectfilter }>
              { f }
          </label>
        </div>

      </div>
      <div class="o-grid__cell o-grid__cell--width-25">

        <i class="material-icons">
        filter_hdr
        </i>
        <input name="filter-range" type="text" class="c-field" placeholder="Range" onfocus={ focusfilter } onkeydown={ focusfilter } />

        <div role="menu" class="c-card c-card--menu u-high">
          <label role="menuitem" class="c-card__control c-field c-field--choice"
            each={ f in filters_shown.range }
            data-target="filter-range" onclick={ selectfilter }>
              { f }
          </label>
        </div>

      </div>
      <div class="o-grid__cell o-grid__cell--width-25">

        <i class="material-icons">
        work
        </i>
        <input name="filter-field" type="text" class="c-field" placeholder="Field" onfocus={ focusfilter } onkeydown={ focusfilter } />

        <div role="menu" class="c-card c-card--menu u-high">
          <label role="menuitem" class="c-card__control c-field c-field--choice"
            each={ f in filters_shown.field }
            data-target="filter-field" onclick={ selectfilter }>
              { f }
          </label>
        </div>

      </div>
      <div class="o-grid__cell o-grid__cell--width-25">

        <i class="material-icons">
        pets
        </i>
        <input name="filter-taxon" type="text" class="c-field" placeholder="Taxon" onfocus={ focusfilter } onkeydown={ focusfilter } />

        <div role="menu" class="c-card c-card--menu u-high">
          <label role="menuitem" class="c-card__control c-field c-field--choice"
            each={ f in filters_shown.taxon }
            data-target="filter-taxon" onclick={ selectfilter }>
              { f }
          </label>
        </div>

      </div>

    </div>
  </form>

  <div class="help" style="margin:1em" hide={ results.items.length }>
    <p>
      To search for research scientists, enter partial names (e.g. Jill)
      or biography keywords (e.g. alpine monitoring ecology), or
      submit it blank to use the filters directly.
      <!-- Use the map below to focus on a geographic region. -->
    </p>
  </div>

  <div class="results" hide={ detailview }>

    <div class="result-count o-field" hide={ !results.items.length }>
      <b class="total">{ results.total}</b> results<span hide={ !results.has_next }>, first
      <b class="top">{ results.items.length }</b> shown</span>
    </div>

    <div class="row" each={ results.items }>
      <a class="person" onclick={ details }>
        <div class="name">{ fullname }</div>
        <span>{ organisation }</span> &nbsp;
      </a>
    </div>

    <div class="footer" hide={ !results.has_next }>
      <button onclick={ nextpage } type="button" class="c-button" title="Show more results">Show more</button>
    </div>
  </div>

  <div class="details" hide={ !detailview }>
    <div class="person c-card">
      <header class="c-card__header">
        <center>
          <button onclick={ closedetails } type="button" class="c-button" title="Close this file">Return to results</button>
        </center>
        <h2 class="c-heading">
          { person.data.fullname }
        </h2>
      </header>
      <div class="c-card__body">
        <p style="font-size: 110%">
          <b>{ person.data.position }</b><br>
          { person.data.organisation }<br>
          { person.data.country }
        </p>
        <a hide={ !person.data.personal_url } href={ person.data.personal_url } target="_blank">{ person.data.personal_url }</a>
        <p>{ person.data.biography }</p>
      </div>
      <footer class="c-card__footer">
        <div class="o-grid">
          <div class="o-grid__cell fields">
            <h5>Fields</h5>
            <ul><li each={ f in person.fields }>{ f }</li></ul>
          </div><div class="o-grid__cell methods">
            <h5>Methods</h5>
            <ul><li each={ f in person.methods }>{ f }</li></ul>
          </div><div class="o-grid__cell scales">
            <h5>Scales</h5>
            <ul><li each={ f in person.scales }>{ f }</li></ul>
          </div><div class="o-grid__cell taxa">
            <h5>Taxa</h5>
            <ul><li each={ f in person.taxa }>{ f }</li></ul>
          </div>
        </div>

        <h2>Resources</h2>
        <ul class="resources">
          <li each={ res in person.resources }>
            <a href={ res.url } target="_blank">
              <b>{ res.title }</b>
            </a>
            <br>{ res.abstract }<br>
            <small>{ res.citation }</small>
          </li>
        </ul>
      </footer>
    </div>
  </div>

  <script>
    this.page = 1
    this.results = { 'items': [] }
    this.detailview = false
    this.person = { 'data': false, 'resources': [] }
    const FILTER_BLANK = {
       'country': [], 'range': [], 'field': [], 'taxon': []
    }
    this.filters_shown = FILTER_BLANK

    search(e, nextpage) {
      e.preventDefault()
      var self = this
      self.closedetails()
      self.clearfilter()

      // Get the value of the search query
      q = $('input[name="query"]').val()

      // Iterate through the filter fields
      $.each(Object.keys(FILTER_BLANK), function() {
        fq = $('input[name="filter-'+this+'"]').val()
        if (fq.length > 2)
          q += '&' + this + '=' + fq
      })

      // Check for page
      current_items = []
      if (typeof(nextpage) !== 'undefined' && nextpage) {
        q += '&page=' + nextpage
        current_items = self.results.items
      }

      // Run a search query
      $.getJSON('/api/search?q=' + q, function(data) {
        self.results = data
        if (current_items.length > 0)
          self.results.items = current_items.concat(self.results.items)
        self.update()
      })
    }

    nextpage(e) {
      if (this.results.items === [] || !this.results.has_next) return
      this.search(e, this.results.page + 1)
    }

    clearfilter(e) {
      var self = this
      $.each(Object.keys(FILTER_BLANK), function() {
        self.filters_shown[this] = []
      })
    }

    resetsearch(e) {
      var self = this
      $('form').each(function() { this.reset() })
      self.clearfilter(e)
      self.results = { 'items': [] }
    }

    focusfilter(e) {
      var self = this
      self.clearfilter()
      if (self.results.items === []) return

      $.each(Object.keys(FILTER_BLANK), function() {
        var filter = this
        fq = $('input[name="filter-' + filter + '"]').val().toLowerCase().trim()
        $.each(self.results.filters[filter], function() {
          if (this.toLowerCase().indexOf(fq) >= 0)
            self.filters_shown[filter].push(this)
        })
      })
    }

    selectfilter(e) {
      if (typeof(e.target) === 'undefined') return
      $obj = $(e.target)
      $tgt = $('input[name="' + $obj.attr('data-target') + '"]')
      $tgt.val($obj.text().trim())
      this.search(e)
    }

    details(e) {
      e.preventDefault()
      var self = this
      pid = e.item.id
      self.person = { 'data': false, 'resources': [] }
      $.getJSON('/api/people/' + pid, function(data) {
        self.detailview = true
        self.person = data
        self.update()
        window.location = '#top'
        window.location = '#person=' + pid
      })
    }

    closedetails(e) {
      this.detailview = false
    }

  </script>

</gmba-search>
