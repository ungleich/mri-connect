(function($) {

	$(function() {

		$container = $('#content')
		$.getJSON('/api/people', function(data) {
			$.each(data, function() {
				$container.append(
					'<div class="3u 6u(narrower) 12u$(mobilep)">' +
					'<h4>' + this.fullname + '</h4>' +
					'<p>' + this.organisation + '</p>' +
					'<a href="' + this.personal + '">Homepage</a></div>'
				);
			});
		});

	});

})(jQuery);
