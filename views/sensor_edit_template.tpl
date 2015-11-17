%include header_template sensors=sensors
%import datetime

	<div id="sensorData">
		<form id="sensorInput" action="/sensor/save/{{sensor['sensorid']}}" method="post">
			<fieldset>
				<label for="enabled">Omogočeno:</label>
				%if sensor['enabled']:
					<input type="checkbox" id="enabled" name="enabled" value="1" checked>
				%else:
					<input type="checkbox" id="enabled" name="enabled" value="1">
				%end

				<label for="name">Naziv:</label>
				<input type="text" id="name" name="name" value="{{sensor['name']}}">
				<label for="threshold">Temperatura gretja:</label>
				<input type="number" id="threshold" name="threshold" min="-10" max="40" value="{{sensor['threshold']}}">
				<label for="automaticmode">Način delovanja:</label>
				<select name="automaticmode">
					<option value="1" {{'selected' if sensor['automatic'] else ''}}>Samodejno</option>
					<option value="0" {{'selected' if not sensor['automatic'] else ''}}>Ročno</option>
				</select>

				<label for="comment">Opis:</label>
				<textarea rows="5" cols="30" id="comment" name="comment">{{sensor['comment']}}</textarea>
			</fieldset>
			
			<input type="submit" class="button" value="Shrani">
		</form>
	</div>

%include footer_template
