<gmba-search>

  <div class="help" style="margin:1em" hide={ results.items.length }>
    <p>
      To search for a scientist, enter partial names (e.g. Jill), organization, position, or leave blank to search by country, range, expertise or taxa. Both the Range filter or the map below can be used to select a mountain range.
    </p>
  </div>

  <form onsubmit={ search } autocomplete="off">

    <div class="o-field o-field--icon-left">
      <i class="material-icons">
        search
      </i>
      <button onclick={ resetsearch } type="button" class="c-button c-button--close" title="Reset search">&times;</button>
      <input name="query" class="c-field" placeholder="Search name, organisation, position" type="text" />
    </div>

  </form>
  <div class="o-grid o-grid--wrap o-grid--small-full o-grid--medium-small o-grid--large-full">

    <div class="o-grid__cell o-grid__cell--width-25">
      <form onsubmit={ search } autocomplete="off">

      <i class="material-icons">
      public
      </i>
      <input name="filter-country" type="text" class="c-field" placeholder="Country" onfocus={ focusfilter } onkeydown={ keydownfilter } />

      <div role="menu" class="c-card c-card--menu u-high">
        <label role="menuitem" class="c-card__control c-field c-field--choice"
          each={ f in filters_shown.country }
          data-target="filter-country" onclick={ selectfilter }>
            { f }
        </label>
      </div>

      </form>
    </div>
    <div class="o-grid__cell o-grid__cell--width-25">
      <form onsubmit={ search } autocomplete="off">

      <i class="material-icons">
      filter_hdr
      </i>
      <input name="filter-range" type="text" class="c-field" placeholder="Range" onfocus={ focusfilter } onkeydown={ keydownfilter } />

      <div role="menu" class="c-card c-card--menu u-high">
        <label role="menuitem" class="c-card__control c-field c-field--choice"
          each={ f in filters_shown.range }
          data-target="filter-range" onclick={ selectfilter }>
            { f }
        </label>
      </div>

      </form>
    </div>
    <div class="o-grid__cell o-grid__cell--width-25">
      <form onsubmit={ search } autocomplete="off">

      <i class="material-icons">
      work
      </i>
      <input name="filter-field" type="text" class="c-field" placeholder="Expertise" onfocus={ focusfilter } onkeydown={ keydownfilter } />

      <div role="menu" class="c-card c-card--menu u-high">
        <label role="menuitem" class="c-card__control c-field c-field--choice"
          each={ f in filters_shown.field }
          data-target="filter-field" onclick={ selectfilter }>
            { f }
        </label>
      </div>

      </form>
    </div>
    <div class="o-grid__cell o-grid__cell--width-25">
      <form onsubmit={ search } autocomplete="off">

      <i class="material-icons">
      pets
      </i>
      <input name="filter-taxon" type="text" class="c-field" placeholder="Taxon" onfocus={ focusfilter } onkeydown={ keydownfilter } />

      <div role="menu" class="c-card c-card--menu u-high">
        <label role="menuitem" class="c-card__control c-field c-field--choice"
          each={ f in filters_shown.taxon }
          data-target="filter-taxon" onclick={ selectfilter }>
            { f }
        </label>
      </div>

      </form>
    </div>

  </div><!-- /o-grid -->

  <div class="noresults" style="margin:1em" hide={ !results.not_found }>
    <h5>
      No results for this search. Please try another query.
    </h5>
  </div>

  <div class="mapview" hide={ detailview || results.items.length }>
    <div id="map"></div>
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
        <div class="c-input-group c-input-group--rounded" style="float:right">
          <button onclick={ closedetails } type="button" class="c-button c-button--success" title="Close this file">Return to results</button>
          <button onclick={ permalink } type="button" class="c-button c-button--brand" title="Permalink">Permalink</button>
          <button href={ person.data.personal_url } target="_blank" type="button" class="c-button c-button--info" title="Website">Website</button>
        </div>
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
        <!-- Hide the bio for now ->->
        <!-- <p>{ person.data.biography }</p> -->
      </div>
      <footer class="c-card__footer">
        <div class="c-card c-card--accordion person-tags">

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Expertise
          </button>
          <section class="c-card__item c-card__item--pane fields">
            <span each={ f in person.fields }>{ f }</span>
          </section>

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Methods
          </button>
          <section class="c-card__item c-card__item--pane methods">
            <span each={ f in person.methods }>{ f }</span>
          </section>

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Scales
          </button>
          <section class="c-card__item c-card__item--pane scales">
            <span each={ f in person.scales }>{ f }</span>
          </section>

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Taxa
          </button>
          <section class="c-card__item c-card__item--pane taxa">
            <span each={ f in person.taxa }>{ f }</span>
          </section>

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Mountain ranges
          </button>
          <section class="c-card__item c-card__item--pane ranges">
            <span each={ f in person.ranges }>{ f.name }</span>
          </section>

          <button role="heading" aria-expanded="false" class="c-card__control" onclick={ toggleaccordion }>
            Resources
          </button>
          <section class="c-card__item c-card__item--pane resources">
            <ul><li each={ res in person.resources }>
              <div class="c-input-group c-input-group--rounded">
                <a href="#" onclick={ openresource } class="c-button u-small c-button--brand" target="_blank">Details</a>
                <a href={ res.url } class="c-button u-small c-button--info" target="_blank">Link</a>
              </div>
              <b>{ res.title }</b>
              <div class="resource-detail" style="display:none">
                <div class="abstract">{ res.abstract }<div>
                <div class="citation">{ res.citation }</div>
              </div>
              <br clear="all">
            </li></ul>
          </section>

        </div><!-- /c-card--accordion -->

        <h2>Contact</h2>
        <form action="https://formspree.io/hi@datalets.ch" b="gmba@ips.unibe.ch" method="POST" class="contact-form">
          <input type="hidden" name="subject" value="Contact request from GMBA Connect">
          <input type="hidden" name="person" value={ person.data.fullname }>
          <textarea name="message" cols="80" rows="3" placeholder="Enter a message"></textarea><br>
          <input type="text" name="name" placeholder="Your name">
          <input type="email" name="_replyto" placeholder="E-mail address">
          <input type="submit" value="Send">
        </form>

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
      this.runsearch(nextpage)
    }

    runsearch(nextpage) {
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
        self.results.not_found = (data.items.length == 0)
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
      this.detailview = false
    }

    focusfilter(e) {
      var self = this
      self.clearfilter()
      if (self.results.items === []) return
      if (!self.results.filters) return

      $.each(Object.keys(FILTER_BLANK), function() {
        var filter = this
        fq = $('input[name="filter-' + filter + '"]').val().toLowerCase().trim()
        $.each(self.results.filters[filter], function() {
          if (this.toLowerCase().indexOf(fq) >= 0)
            self.filters_shown[filter].push(this)
        })
      })
    }

    keydownfilter(e) {
      // TODO: json call to fetch more data
      this.focusfilter(e)
    }

    toggleaccordion(e) {
      $obj = $(e.target)
      $obj.attr('aria-expanded', ''+$obj.attr('aria-expanded')!='true')
    }

    openresource(e) {
      e.preventDefault()
      $obj = $(e.target)
      $obj.parent().parent().find('.resource-detail').toggle();
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

    permalink(e) {
      $obj = $(e.target)
      console.log($obj)
    }

    this.on('mount', function() {
      var self = this;
			var mymap = L.map('map').setView([51.505, -0.09], 2)

			L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
				maxZoom: 18,
				attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
					'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
					'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
				id: 'mapbox.streets'
			}).addTo(mymap)

			var mountain_ranges = new L.GeoJSON.AJAX("/static/geodata/gmba.geojson")
      // TODO: reduce weight of line style
			mountain_ranges.addTo(mymap)
      mountain_ranges.on('click', function(e) {
        $('input[name="filter-range"]').val(e.layer.feature.properties.Name)
        self.runsearch()
      })
    })

  </script>

</gmba-search>
