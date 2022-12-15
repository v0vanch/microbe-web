#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Сброс" %>
<%in p/header.cgi %>

<div class="row row-cols-md-3 g-4 mb-4">
  <div class="col">
    <div class="alert alert-danger">
      <h4>Перезагрузка камеры</h4>
      <p>Перезагрузите камеру, чтобы новые настройки вступили в силу. Также это удалит все данные на разделах смонтированных в системную память, например, /tmp.</p>
      <% button_reboot %>
    </div>
  </div>
  <div class="col">
    <%in p/reset-firmware.cgi %>
  </div>
  <div class="col">
    <div class="alert alert-danger">
      <h4>Сброс настроек Majestic</h4>
      <p>Сбросьте конфигурацию Majestic <code>/etc/majestic.yaml</code> до исходного состояния. Все изменения будут утеряны!
       Перед сбросом следует <a href="majestic-config-actions.cgi">сделать бэкап текущей конфигурации</a>.</p>
      <% button_mj_reset %>
    </div>
  </div>
</div>

<%in p/footer.cgi %>
