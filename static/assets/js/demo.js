(function($) {

	$(function() {

		$container = $('#content')
		$detail = $('#detail')

		refresh_content = function(data) {
			$container.empty();
			$.each(data.items, function() {
				$container.append(
					'<div class="person">' +
					'<h4>' + this.fullname + '</h4>' +
					'<span>' + this.organisation + '</span> &nbsp;' +
					'<a class="c-button c-button--brand u-small" href="' + this.personal + '">Details</a>' +
					'</div>'
				).find('a:last').data('person-id', this.id).click(function(e) {
					e.preventDefault(); e.stopPropagation();
					$container.addClass('hide');
					$.getJSON('/api/people/' + $(this).data('person-id'), function(data) {
						var person = data.data, resources = data.resources;
						$detail.html(
							'<div class="person">' +
							'<button class="btn btn-success">Back</button>' +
							'<h4>' + person.fullname + '</h4>' +
							'<p>' + person.position + '</p>' +
							'<h5>' + person.organisation + '</h5>' +
							'<p>' + person.country + '</p>' +
							'<p>' + person.biography + '</p>' +
							'<p><a target="_blank" href="' + this.personal_url + '">Website</a></p>' +
							'<div class="resources"></div>' +
							'</div>').removeClass('hide').find('button').click(function() {
								$detail.addClass('hide');
								$container.removeClass('hide');
							});
						$resources = $detail.find('.resources');
						$.each(resources, function() {
							$resources.append(
								'<li><a href="' + this.url + '" target="_blank">' +
								'<b>' + this.title + '</b></a>' +
								'<br>' + this.abstract + '<br>' +
								'<small>' + this.citation + '</small>' +
								'</li>'
							);
						}); //- each resources
					}); //- getJSON
				}); //- click
			}); //- each
		}; //- refresh_content

		// $.getJSON('/api/people', refresh_content); //- getJSON

		var delay = (function(){
		  var timer = 0;
		  return function(callback, ms){
		    clearTimeout (timer);
		    timer = setTimeout(callback, ms);
		  };
		})();
		$('input[name="query"]').on('input', function() {
			var q = $(this).val().toLowerCase();
			if (q.length < 3) return $container.addClass('hide');
			delay(function() {
				// console.log(q);
				$('#help').hide();
				$container.removeClass('hide');
				$detail.addClass('hide');
				$.getJSON('/api/search?q=' + q, refresh_content); //- getJSON
			}, 100);
		});

		$('#show-advanced').click(function() { $('#advanced').show() });

		var mymap = L.map('map').setView([51.505, -0.09], 1);

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
			maxZoom: 18,
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
				'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
				'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			id: 'mapbox.streets'
		}).addTo(mymap);

		var mountain_ranges = new L.GeoJSON.AJAX("/data/gmba.geojson");
		mountain_ranges.addTo(mymap);

	});

})(jQuery);

riot.mount('gmba-search');
