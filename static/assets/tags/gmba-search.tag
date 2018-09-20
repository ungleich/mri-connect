<gmba-search>

  <form onsubmit={ search }>

    <input name="query" class="c-field" placeholder="Search ..." type="text" />

    <!-- <a href="#" class="button c-button" id="show-advanced">Advanced search</a> -->
<!--
    <select onchange={ refine(country) } class="c-field">
      <option each={ filters.country }></option>
    </select> -->

    <!-- <select onchange={ refine(range) }>
      <option each={ filters.range }></option>
    </select>

    <select onchange={ refine(expertise) }>
      <option each={ filters.expertise }></option>
    </select>

    <select onchange={ refine(taxa) }>
      <option each={ filters.taxa }></option>
    </select> -->

  </form>

  <div class="help">
    <p>
      To search for research scientists, enter partial names (e.g. Dr. Jill)
      or research field keywords (e.g. alpine monitoring ecology).
      You can also use the map below to focus on a geographic region.
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
    <div class="person">
      <button class="c-button c-button--brand" onclick={ closedetails }>
        Close</button>
      <h4>{ person.data.fullname }</h4>
      <p>{ person.data.position }</p>
      <h5>{ person.data.organisation }</h5>
      <p>{ person.data.country }</p>
      <p>{ person.data.biography }</p>
      <p>
        <a target="_blank" href={ person.data.personal_url }>Website</a>
      </p>
      <ul class="resources">
        <li each={ res in person.resources }>
          <a href={ res.url } target="_blank">
            <b>{ res.title }</b>
          </a>
          <br>{ res.abstract }<br>
          <small>{ res.citation }</small>
        </li>
      </ul>
    </div>
  </div>

  <script>
    this.results = {}
    this.detailview = false
    this.person = { 'data': false, 'resources': [] }

    // var results = riot.observable()

    search(e) {
      e.preventDefault()
      var self = this
      q = $('input[name="query"]').val()
      $.getJSON('/api/search?q=' + q, function(data) {
        self.results = { 'people': data.items }
        self.update()
      })
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
