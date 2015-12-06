<!DOCTYPE HTML>
<html lang="sl">
<head>
        <meta charset="utf-8"> 
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Termo</title>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">
        <link rel="stylesheet" href="/static/css/bootstrap-datepicker3.min.css">
        <link rel="stylesheet" href="/static/css/bootstrap-timepicker.min.css">
        <link rel="stylesheet" href="/static/css/termo.css">
</head>
<body>
        <nav class="navbar navbar-inverse">
                <div class="navbar-header">
                        <a class="navbar-brand" href="#"><span class="glyphicon glyphicon-cloud"></span>&nbsp;&nbsp;Termo</a>
                </div>
                <div>
                        <ul class="nav navbar-nav">
                                <li class="{{'active' if activepage == 'overview' else ''}}"><a href="/sensor/0">Pregled</a></li>
                                <li class="{{'active' if activepage == 'setup' else ''}}"><a href="/sensor/edit/0">Nastavitve</a></li>
                        </ul>
                </div>
        </nav>

