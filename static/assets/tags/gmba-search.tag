<gmba-search>

  <form onsubmit={ search }>
    <div class="o-field o-field--icon-left">
      <i class="material-icons">
        search
      </i>
      <input name="query" class="c-field" placeholder="Search ..." type="text" />
    </div>
  </form>

  <div class="o-grid o-grid--wrap field-filters">
    <form onsubmit={ search } autocomplete="off">

      <div class="o-grid__cell">

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
    </form><form onsubmit={ search }>
      <div class="o-grid__cell">

        <i class="material-icons">
        filter_hdr
        </i>
        <input name="filter-range" type="text" class="c-field" placeholder="Range" />

                <div role="menu" class="c-card c-card--menu u-high">
                  <label role="menuitem" class="c-card__control c-field c-field--choice"
                    each={ f in filters_shown.range }
                    data-target="filter-range" onclick={ selectfilter }>
                      { f }
                  </label>
                </div>

      </div>
    </form><form onsubmit={ search }>
      <div class="o-grid__cell">

        <i class="material-icons">
        work
        </i>
        <input name="filter-field" type="text" class="c-field" placeholder="Field" />

                <div role="menu" class="c-card c-card--menu u-high">
                  <label role="menuitem" class="c-card__control c-field c-field--choice"
                    each={ f in filters_shown.field }
                    data-target="filter-field" onclick={ selectfilter }>
                      { f }
                  </label>
                </div>

      </div>
    </form><form onsubmit={ search }>
      <div class="o-grid__cell">

        <i class="material-icons">
        pets
        </i>
        <input name="filter-taxon" type="text" class="c-field" placeholder="Taxon" />

                <div role="menu" class="c-card c-card--menu u-high">
                  <label role="menuitem" class="c-card__control c-field c-field--choice"
                    each={ f in filters_shown.taxon }
                    data-target="filter-taxon" onclick={ selectfilter }>
                      { f }
                  </label>
                </div>

        <!--<select class="c-field" filter-type="taxa" placeholder="Taxa">
          <option each={ filters.taxa }>{ name }</option>
        </select>-->

      </div>
    </form>
  </div>

  <!--<div role="menu" class="c-card c-card--menu u-high c-card--grouped">
  <button role="menuitem" class="c-card__control">Proposition 1</button>
  <button role="menuitem" class="c-card__control">Proposition 2</button>
  <button role="menuitem" class="c-card__control">Proposition 3</button>
  <button role="menuitem" class="c-card__control">Proposition 4</button>
  <button role="menuitem" class="c-card__control">Proposition 5</button>
  <button role="menuitem" class="c-card__control">Proposition 6</button>
</div>-->

  <div class="help" style="margin:1em" hide={ results.people }>
    <p>
      To search for research scientists, enter partial names (e.g. Jill)
      or research field keywords (e.g. alpine monitoring ecology), or
      you even submit it blank to use the filters.
      Use the map below to focus on a geographic region.
    </p>
  </div>
  <div class="results" hide={ detailview }>
    <div class="person" each={ results.people }>
      <a href={ url } onclick={ details }>
        <h4>{ fullname }</h4>
        <span>{ organisation }</span> &nbsp;
      </a>
    </div>
  </div>
  <div class="details" hide={ !detailview }>
    <div class="person c-card">
      <header class="c-card__header">
        <button onclick={ closedetails } type="button" class="c-button c-button--close" title="Close">&times;</button>
        <h2 class="c-heading">
          { person.data.fullname }
        </h2>
      </header>
      <div class="c-card__body">
        <a hide={ !person.data.personal_url } href={ person.data.personal_url } class="c-button c-button--brand" target="_blank">Website</a>
        <h4>
          { person.data.position }<br>
          { person.data.organisation }<br>
          { person.data.country }
        </h4>
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
    this.results = {}
    this.detailview = false
    this.person = { 'data': false, 'resources': [] }
    const FILTER_BLANK = {
       'country': [], 'range': [], 'field': [], 'taxon': []
    }
    this.filters_shown = FILTER_BLANK
    this.filters_available = FILTER_BLANK

    search(e) {
      e.preventDefault()
      var self = this
      self.clearfilter()

      // Get the value of the search query
      q = $('input[name="query"]').val()

      // Iterate through the filter fields
      $.each(Object.keys(FILTER_BLANK), function() {
        fq = $('input[name="filter-'+this+'"]').val()
        if (fq.length > 2)
          q += '&' + this + '=' + fq
      })

      // Run a search query
      $.getJSON('/api/search?q=' + q, function(data) {
        self.results = { 'people': data.items }
        self.filters_available = data.filters
        self.update()
      })
    }

    clearfilter(e) {
      var self = this
      $.each(Object.keys(FILTER_BLANK), function() {
        self.filters_shown[this] = []
      })
    }

    focusfilter(e) {
      var self = this
      self.clearfilter()
      if (self.filters_available === {}) return

      $.each(Object.keys(FILTER_BLANK), function() {
        var filter = this
        fq = $('input[name="filter-' + filter + '"]').val().toLowerCase().trim()
        $.each(self.filters_available[filter], function() {
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
      $.getJSON('/api/people/' + pid, function(data) {
        self.person = data
        self.detailview = true
        self.update()
      })
    }

    closedetails(e) {
      this.detailview = false
    }

  </script>

</gmba-search>
