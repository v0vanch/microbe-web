#!/usr/bin/haserl
Content-type: text/html; charset=UTF-8
Date: <%= $(TZ=GMT0 date +'%a, %d %b %Y %T %Z') %>
Server: <%= $SERVER_SOFTWARE %>
Cache-Control: no-store
Pragma: no-cache

<!DOCTYPE html>
<html lang="<%= $locale %>">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title><% html_title %></title>
<link rel="stylesheet" href="/a/bootstrap.css">
<link rel="stylesheet" href="/a/bootstrap.override.css">
<script src="/a/bootstrap.js"></script>
<script src="/a/main.js"></script>
</head>

<body id="page-<%= $pagename %>" class="<%= $fw_variant %><% [ "$debug" -ge "1" ] && echo -n " debug" %>">
  <nav class="navbar bg-white shadow-sm navbar-expand-lg mb-2">
    <div class="container">
      <a class="navbar-brand" href="status.cgi"><img alt="Image: OpenIPC logo" height="32" src="/a/logo.svg">
        <!--<span class="x-small ms-3"><%= $fw_variant %></span></a>-->
      <% if [ -n "$soc_temp" ]; then %>
        <span id="soc-temp" class="text-white bg-primary rounded small" title="<%= $tSoCTemp %>"><%= $soc_temp %>°C</span>
      <% fi %>
      <button aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler" data-bs-target="#navbarNav" data-bs-toggle="collapse" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownInformation" role="button">Инфо</a>
            <ul aria-labelledby="dropdownInformation" class="dropdown-menu">
              <li><a class="dropdown-item" href="status.cgi">Статус</a></li>
              <li><a class="dropdown-item" href="info-cron.cgi">Настройки Cron</a></li>
              <li><a class="dropdown-item" href="info-dmesg.cgi">Диагностические сообщения</a></li>
              <li><a class="dropdown-item" href="info-httpd.cgi">HTTPd среда</a></li>
              <li><a class="dropdown-item" href="info-modules.cgi">Модули</a></li>
              <li><a class="dropdown-item" href="info-netstat.cgi">Статистика сети</a></li>
              <li><a class="dropdown-item" href="info-log.cgi">Логи</a></li>
              <li><a class="dropdown-item" href="info-overlay.cgi">Раздел оверлея</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownUpdates" role="button">Обновления</a>
            <ul aria-labelledby="dropdownUpdates" class="dropdown-menu">
              <li><a class="dropdown-item" href="firmware.cgi">Прошивка</a></li>
              <li><a class="dropdown-item" href="webui.cgi">Веб-интефейс</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownSettings" role="button">Настройки</a>
            <ul aria-labelledby="dropdownSettings" class="dropdown-menu">
              <li><a class="dropdown-item" href="network.cgi">Сеть</a></li>
              <li><a class="dropdown-item" href="timezone.cgi">Временная зона</a></li>
              <li><a class="dropdown-item" href="network-ntp.cgi">Синхронизация времени</a></li>
              <li><a class="dropdown-item" href="network-socks5.cgi">SOCKS5 Прокси</a></li>
              <li><a class="dropdown-item" href="webui-settings.cgi">Веб-интерфейс</a></li>
              <li><a class="dropdown-item" href="admin.cgi">Профиль админа</a></li>
              <li><a class="dropdown-item" href="debugging.cgi">Отладка</a></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="reset.cgi">Сброс...</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownMajestic" role="button">Majestic</a>
            <ul aria-labelledby="dropdownMajestic" class="dropdown-menu">
<%
mj=$(echo "$mj" | sed "s/ /_/g")
for _line in $mj; do
  _parameter=${_line%%|*};
  _param_name=${_parameter#.};
  _param_domain=${_param_name%.*}
  if [ "$_parameter_domain_old" != "$_param_domain" ]; then
    # hide certain domains if not supported
    [ -n "$(eval echo "\$mj_hide_${_param_domain}" | sed -n "/\b${soc_family}\b/p")" ] && continue
    [ -n "$(eval echo "\$mj_show_${_param_domain}_vendor")" ] && [ -z "$(eval echo "\$mj_show_${_param_domain}_vendor" | sed -n "/\b${soc_vendor}\b/p")" ] && continue
    _parameter_domain_old="$_param_domain"
    _css="class=\"dropdown-item\""; [ "$_param_domain" = "$only" ] && _css="class=\"dropdown-item active\" aria-current=\"true\""
    echo "<li><a ${_css} href=\"majestic-settings.cgi?tab=${_param_domain}\">$(eval echo \$tT_mj_${_param_domain})</a></li>"
  fi
done
unset _css; unset _param_domain; unset _line; unset _param_name; unset _parameter_domain_old; unset _parameter;
%>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="info-majestic.cgi">Majestic YAML</a></li>
              <li><a class="dropdown-item" href="majestic-config-actions.cgi">Обслуживание Majestic</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownTools" role="button">Tools</a>
            <ul aria-labelledby="dropdownTools" class="dropdown-menu">
              <li><a class="dropdown-item" href="tools.cgi">Ping & Traceroute</a></li>
              <li><a class="dropdown-item" href="console.cgi">Веб консоль</a></li>
              <li><a class="dropdown-item" href="ssh-keys.cgi">SSH ключ</a></li>
              <li><a class="dropdown-item" href="sdcard.cgi">SD карта</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownServices" role="button">Сервисы</a>
            <ul aria-labelledby="dropdownServices" class="dropdown-menu">
              <% load_plugins %>
            </ul>
          </li>
          <li class="nav-item"><a class="nav-link" href="preview.cgi">Камера</a></li>
          <li class="nav-item dropdown">
            <a aria-expanded="false" class="nav-link dropdown-toggle" data-bs-toggle="dropdown" href="#" id="dropdownHelp" role="button">Помощь</a>
            <ul aria-labelledby="dropdownHelp" class="dropdown-menu dropdown-menu-lg-end">
              <li><a class="dropdown-item" href="https://openipc.org/">About OpenIPC</a></li>
              <li><a class="dropdown-item" href="https://openipc.org/majestic-endpoints">Majestic Endpoints</a></li>
              <li><a class="dropdown-item" href="https://openipc.org/wiki/">OpenIPC Wiki</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <main class="pb-4">
    <div class="container" style="min-height: 90vh">
      <p class="text-end x-small"><%= $(signature) %></p>

<% if [ -z "$network_gateway" ]; then %>
<div class="alert alert-warning">
<p class="mb-0">Нет соединения с интернетом. Пожалуйста, <a href="network.cgi">проверьте настройки сети</a>.</p>
</div>
<% fi %>

<% if [ "true" = "$openwall_socks5_enabled" ] || [ "true" = "$telegram_socks5_enabled" ] || [ "true" = "$yadisk_socks5_enabled" ]; then
  if [ -z "$socks5_host" ] || [ -z "$socks5_port" ]; then %>
<div class="alert alert-danger">
<p class="mb-0">SOCKS5 прокси включен, но не настроен! Пожалуйста, <a href="network-socks5.cgi">настройте прокси</a>.</p>
</div>
<% fi; fi %>

<% if [ "true" = "$speaker_enabled" ] && [ "true" != "$(yaml-cli -g .audio.enabled)" ]; then %>
<div class="alert alert-danger">
<p class="mb-0">Необходимо включить аудио в <a href="majestic-settings.cgi?tab=audio">настройках Majestic.</a></p>
</div>
<% fi %>

<% if [ "$(cat /etc/TZ)" != "$TZ" ]; then %>
<div class="alert alert-danger">
<p>$TZ переменная в системной среде нуждается в обновлении!</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Перезагрузить камеру</a>
<a class="btn btn-primary" href="timezone.cgi">Настройки временной зоны</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/network-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Настройки сети были обновлены. Перезагрузите камеру, чтобы изменения вступили в силу.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Перезагрузить камеру</a>
<a class="btn btn-primary" href="network.cgi">Настройки сети</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/coredump-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Настройки отладки Majestic были обновлены. Перезагрузите камеру, чтобы изменения вступили в силу.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Перезагрузить камеру</a>
<a class="btn btn-primary" href="debugging.cgi">Настройки отладки</a>
</span>
</div>
<% fi %>

<% if [ -f /tmp/motionguard-restart.txt ]; then %>
<div class="alert alert-danger">
<p>Настройки отслеживания движения были обновлены. Перезагрузите камеру, чтобы изменения вступили в силу.</p>
<span class="d-flex gap-3">
<a class="btn btn-danger" href="reboot.cgi">Перезагрузить камеру</a>
<a class="btn btn-primary" href="plugin-motion.cgi">Настройки отслеживания движения</a>
</span>
</div>
<% fi %>

<h2><%= $page_title %></h2>
<% flash_read %>
