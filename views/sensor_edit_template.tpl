%include header_template sensors=sensors
%import datetime

<div class="container">
	<form id="sensorInput" role="form" action="/sensor/save/{{sensor['sensorid']}}" method="post">
		<div class="form-group">
			<label for="enabled">Omogočeno:</label>
			%if sensor['enabled']:
				<input type="checkbox" id="enabled" name="enabled" value="1" checked>
			%else:
				<input type="checkbox" id="enabled" name="enabled" value="1">
			%end
		</div>

		<div class="form-group">
			<label for="name">Naziv:</label>
			<input type="text" id="name" name="name" class="form-control" value="{{sensor['name']}}">
		</div>
		<div class="form-group">
			<label for="threshold">Temperatura gretja:</label>
			<input type="number" id="threshold" name="threshold" class="form-control" min="-10" max="40" value="{{sensor['threshold']}}">
		</div>
		<div class="form-group">
			<label for="automaticmode">Način delovanja:</label>
			<select name="automaticmode" class="form-control" >
				<option value="1" {{'selected' if sensor['automatic'] else ''}}>Samodejno</option>
			<option value="0" {{'selected' if not sensor['automatic'] else ''}}>Ročno</option>
			</select>
		</div>

		<div class="form-group">
			<label for="comment">Opis:</label>
			<textarea rows="5" cols="30" id="comment" name="comment" class="form-control" >{{sensor['comment']}}</textarea>
		</div>
		
		<input type="submit" class="btn btn-primary" value="Shrani">
	</form>
</div>

%include footer_template
