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
  <div class="results" each={ results.people }>
    <div class="person">
      <h4>{ fullname }</h4>
      <span>{ organisation }</span> &nbsp;
      <a class="c-button c-button--brand u-small">Details</a>
    </div>
  </div>
  <div class="details">
    <!-- '<div class="person">' +
    '<button class="btn btn-success">Back</button>' +
    '<h4>' + person.fullname + '</h4>' +
    '<p>' + person.position + '</p>' +
    '<h5>' + person.organisation + '</h5>' +
    '<p>' + person.country + '</p>' +
    '<p>' + person.biography + '</p>' +
    '<p><a target="_blank" href="' + this.personal_url + '">Website</a></p>' +
    '<div class="resources"></div>' +
    '</div>' -->
  </div>

  <script>
    this.results = {}

    search(e) {
      e.preventDefault()
      q = e.target.value
      self.results = this.results
      $.getJSON('/api/search?q=' + q, function(data) {
        self.results = data.items
      }); //- getJSON

    }
  </script>

</gmba-search>
