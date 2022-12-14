#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Device status" %>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Камера</h3>
    <h5>Hardware</h5>
    <dl class="small list">
      <dt>Процессор</dt>
      <dd><%= $soc %></dd>
      <dt>Семейство</dt>
      <dd><%= $soc_family %></dd>
      <dt>Сенсор</dt>
      <dd><%= $sensor_ini %></dd>
      <dt>Память</dt>
      <dd><%= $flash_size %> MB</dd>
    </dl>
  </div>

  <div class="col">
    <h3>Система</h3>
    <h5>Прошивка</h5>
    <dl class="small list">
      <dt>Версия</dt>
      <dd><%= "${fw_version}-${fw_variant}" %></dd>
      <dt>Сборка</dt>
      <dd><%= $fw_build %></dd>
      <dt>Majestic</dt>
      <dd><%= $mj_version %></dd>
      <dt>Имя устройства</dt>
      <dd><%= $network_hostname %></dd>
    </dl>
  </div>

  <div class="col">
    <h3>Дата и Время</h3>
    <% ex "/bin/date" %>
    <div class="d-grid d-xxl-flex gap-2 mx-auto">
      <a href="timezone.cgi" class="btn btn-primary">Change timezone</a>
      <a href="network-ntp.cgi" class="btn btn-primary">Set up time synchronization</a>
    </div>
  </div>
</div>

<div class="row g-4 mb-4">
  <div class="col ">
    <h3>Ресурсы</h3>
    <% ex "/usr/bin/uptime" %>
    <% ex "df -T" %>
    <% ex "cat /proc/meminfo | grep Mem" %>
  </div>
  <div class="col">
    <h3>Top 20 Процессов</h3>
    <% ex "top -n 1 -b | sed '/top -n/d' | sed '1,4d' | head -20" %>
  </div>
</div>

<%in p/footer.cgi %>
