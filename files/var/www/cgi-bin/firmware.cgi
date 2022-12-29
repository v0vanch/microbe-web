#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Прошивка"
if [ -n "$network_gateway" ]; then
  fw_date=$(date -D "%a, %d %b %Y %T GMT" +"2.2.%m.%d" --date "$(curl -ILs https://github.com/OpenIPC/firmware/releases/download/latest/openipc.${soc}-br.tgz | grep Last-Modified | cut -d' ' -f2-)")
else
  fw_date="<span class=\"text-danger\">- нет доступа к GitHub -</span>"
fi
fw_kernel="true"
fw_rootfs="true"
%>
<%in p/header.cgi %>

<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
  <div class="col">
    <h3>Версия</h3>
      <dl class="small">
      <dt>Установленная</dt>
      <dd><%= $fw_version %></dd>
      <% if [ -n "$GET_github" ]; then %>
      <dt>На GitHub</dt>
      <dd id="firmware-master-ver"><%= $fw_date %></dd>
      <% fi %>
    </dl>
  </div>
  <% if [ -n "$GET_github" ]; then %>
  <div class="col">
    <h3>Обновление</h3>
    <% if [ -n "$network_gateway" ]; then %>
      <form action="firmware-update.cgi" method="post">
        <% field_checkbox "fw_kernel" "Обновить ядро." %>
        <% field_checkbox "fw_rootfs" "Обновить корневую файловую систему." %>
        <% field_checkbox "fw_reset" "Сбросить прошивку." %>
        <% field_checkbox "fw_noreboot" "Не перезагружать систему после обновления." %>
        <% field_checkbox "fw_enforce" "Установить, даже если версия не поменялась." %>
        <% button_submit "Установить обновление с GitHub" "warning" %>
      </form>
    <% else %>
      <p class="alert alert-danger">Для обновления требуется доступ к GitHub.</p>
    <% fi %>
  </div>
  <% fi %>
  <div class="col">
    <h3>Загрузить ядро & RootFS</h3>
    <form action="firmware-upload-parts.cgi" method="post" enctype="multipart/form-data">
      <% field_file "parts_file" "Бинарный файл" %>
      <% field_select "parts_type" "Тип бинарного файла" "kernel,rootfs" %>
      <p class="text-danger small">Опасное действие! Убедитесь, что вы знаете, что делаете.</p>
      <% button_submit "Загрузить файл" "danger" %>
    </form>
  </div>
</div>

<%in p/footer.cgi %>
