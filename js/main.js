document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('open');
      var expanded = links.classList.contains('open');
      toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { links.classList.remove('open'); });
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var btn = item.querySelector('.faq-q');
    var panel = item.querySelector('.faq-a');
    if (!btn || !panel) return;
    btn.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (other) {
        if (other !== item) {
          other.classList.remove('open');
          other.querySelector('.faq-a').style.maxHeight = null;
          other.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
        }
      });
      if (isOpen) {
        item.classList.remove('open');
        panel.style.maxHeight = null;
        btn.setAttribute('aria-expanded', 'false');
      } else {
        item.classList.add('open');
        panel.style.maxHeight = panel.scrollHeight + 24 + 'px';
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  initEventsCalendar();
});

// ---------------------------------------------------------------------------
// Events calendar + monthly event list.
// ---------------------------------------------------------------------------
function initEventsCalendar() {
  var grid = document.getElementById('cal-grid');
  if (!grid) return;

  var EVENT_META = {
    'pranic-self-care-practices':      { name: 'Pranic Self-Care Practices',            short: 'Self-Care Practices', mode: 'online' },
    'mass-pranic-healing':             { name: 'Mass Pranic Healing',                    short: 'Mass Healing', mode: 'online' },
    'introduction-to-pranic-healing':  { name: 'Introduction to Pranic Healing',         short: 'Intro to Pranic Healing', mode: 'online' },
    'twin-hearts-meditation':          { name: 'Meditation on the Twin Hearts',          short: 'Twin Hearts Meditation', mode: 'online' },
    'community-catchup':               { name: 'Community Catchup',                      short: 'Community Catch-up', mode: 'online' },
    'group-meditation-free-healing':   { name: 'Group Meditation & Free Healing',         short: 'Group Meditation & Free healing', mode: 'offline' },
    'pranic-healing-intro':            { name: 'Introduction to Pranic Healing',          short: 'Intro to Pranic Healing', mode: 'offline' },
    'full-moon-meditation':            { name: 'Full Moon Group Meditation Circle',       short: 'Full Moon Group Meditation', mode: 'offline' }
  };

  var WEEKDAY_EVENTS = {
    1: ['pranic-self-care-practices'],
    2: ['mass-pranic-healing'],
    3: ['introduction-to-pranic-healing'],
    4: ['twin-hearts-meditation'],
    5: ['community-catchup'],
    0: ['group-meditation-free-healing']
  };

  var monthLabel = document.getElementById('cal-month-label');
  var basePath = grid.getAttribute('data-base') || '';
  var shell = grid.closest('.cal-shell');
  var today = new Date();
  var viewYear = today.getFullYear();
  var viewMonth = today.getMonth();
  var activeMode = 'all';
  var popover = null;

  function lastWeekdayOfMonth(year, month, weekday) {
    var d = new Date(year, month + 1, 0);
    while (d.getDay() !== weekday) d.setDate(d.getDate() - 1);
    return d.getDate();
  }

  function eventsForDate(year, month, dateNum) {
    var d = new Date(year, month, dateNum);
    var weekday = d.getDay();
    var slugs = (WEEKDAY_EVENTS[weekday] || []).slice();
    if (weekday === 5 && dateNum === lastWeekdayOfMonth(year, month, 5)) slugs.push('pranic-healing-intro');
    if (weekday === 6 && dateNum === lastWeekdayOfMonth(year, month, 6)) slugs.push('full-moon-meditation');
    if (activeMode !== 'all') slugs = slugs.filter(function (slug) { return EVENT_META[slug].mode === activeMode; });
    return slugs;
  }

  function dateListForSlug(slug, year, month) {
    var dates = [];
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    for (var day = 1; day <= daysInMonth; day++) {
      if (eventsForDate(year, month, day).indexOf(slug) !== -1) dates.push(day);
    }
    return dates;
  }

  function formatDates(slug) {
    var dates = dateListForSlug(slug, viewYear, viewMonth);
    if (!dates.length) return 'Not scheduled this month';
    var monthShort = new Date(viewYear, viewMonth, 1).toLocaleDateString(undefined, { month: 'short' });
    return dates.map(function (d) { return monthShort + ' ' + d; }).join(' · ');
  }

  function closePopover() {
    if (popover) {
      popover.remove();
      popover = null;
    }
    grid.querySelectorAll('.cal-cell.selected').forEach(function (c) { c.classList.remove('selected'); });
  }

  function showPopover(cell, year, month, dateNum) {
    closePopover();
    cell.classList.add('selected');
    var slugs = eventsForDate(year, month, dateNum);
    var dateObj = new Date(year, month, dateNum);
    var label = dateObj.toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });
    popover = document.createElement('div');
    popover.className = 'cal-day-popover';
    popover.setAttribute('role', 'dialog');
    popover.innerHTML = '<button type="button" class="cal-popover-close" aria-label="Close">×</button><h4>' + label + '</h4>';

    if (!slugs.length) {
      popover.innerHTML += '<p class="small">No scheduled sessions on this day.</p>';
    } else {
      var list = document.createElement('ul');
      list.className = 'cal-popover-list';
      slugs.forEach(function (slug) {
        var meta = EVENT_META[slug];
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = basePath + 'events/' + slug + '.html';
        a.innerHTML = '<span class="chip ' + (meta.mode === 'offline' ? 'chip-offline' : 'chip-online') + '">' + (meta.mode === 'offline' ? 'In-person' : 'Online') + '</span>' + meta.name + ' <span class="popover-arrow">→</span>';
        li.appendChild(a);
        list.appendChild(li);
      });
      popover.appendChild(list);
    }
    shell.appendChild(popover);
    popover.querySelector('.cal-popover-close').addEventListener('click', closePopover);

    var shellRect = shell.getBoundingClientRect();
    var cellRect = cell.getBoundingClientRect();
    var left = cellRect.left - shellRect.left + cell.offsetWidth / 2;
    var top = cellRect.top - shellRect.top + cell.offsetHeight + 10;
    popover.style.left = Math.max(10, Math.min(left, shell.clientWidth - 10)) + 'px';
    popover.style.top = top + 'px';

    requestAnimationFrame(function () {
      var rect = popover.getBoundingClientRect();
      var parentRect = shell.getBoundingClientRect();
      if (rect.right > parentRect.right - 10) popover.style.left = (shell.clientWidth - popover.offsetWidth - 10) + 'px';
      if (rect.left < parentRect.left + 10) popover.style.left = '10px';
      if (rect.bottom > parentRect.bottom - 10) {
        popover.style.top = Math.max(10, cell.offsetTop - popover.offsetHeight - 10) + 'px';
      }
    });
  }

  function updateListDates() {
    document.querySelectorAll('.event-row[data-event-slug]').forEach(function (row) {
      var slug = row.getAttribute('data-event-slug');
      var when = row.querySelector('.when');
      if (when && EVENT_META[slug]) when.textContent = formatDates(slug);
    });
  }

  function render() {
    var monthNames = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    if (monthLabel) monthLabel.textContent = monthNames[viewMonth] + ' ' + viewYear;
    closePopover();
    var firstOfMonth = new Date(viewYear, viewMonth, 1);
    var firstWeekdayMonFirst = (firstOfMonth.getDay() + 6) % 7;
    var daysInMonth = new Date(viewYear, viewMonth + 1, 0).getDate();
    var cells = '';
    for (var i = 0; i < firstWeekdayMonFirst; i++) cells += '<div class="cal-cell empty" aria-hidden="true"></div>';
    var isCurrentMonth = viewYear === today.getFullYear() && viewMonth === today.getMonth();
    for (var day = 1; day <= daysInMonth; day++) {
      var slugs = eventsForDate(viewYear, viewMonth, day);
      var isToday = isCurrentMonth && day === today.getDate();
      var eventNames = slugs.map(function (slug) {
        var meta = EVENT_META[slug];
        var cls = meta.mode === 'offline' ? 'offline' : 'online';
        return '<span class="cal-event-name ' + cls + '" title="' + meta.name + '">' + (meta.short || meta.name) + '</span>';
      }).join('');
      cells += '<button type="button" class="cal-cell' + (isToday ? ' today' : '') + (slugs.length ? ' has-events' : '') + '" data-day="' + day + '" aria-label="' + day + ', ' + slugs.length + ' session' + (slugs.length === 1 ? '' : 's') + '"><span class="cal-num">' + day + '</span><span class="cal-events">' + eventNames + '</span></button>';
    }
    grid.innerHTML = cells;
    grid.querySelectorAll('.cal-cell:not(.empty)').forEach(function (cell) {
      cell.addEventListener('click', function () {
        showPopover(cell, viewYear, viewMonth, parseInt(cell.getAttribute('data-day'), 10));
      });
    });
    updateListDates();
  }

  render();

  var viewToggleBtns = document.querySelectorAll('[data-view-target]');
  viewToggleBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var targetView = btn.getAttribute('data-view-target');
      document.querySelectorAll('.view-panel').forEach(function (panel) {
        panel.classList.toggle('active', panel.getAttribute('data-view') === targetView);
      });
      viewToggleBtns.forEach(function (b) { b.classList.toggle('active', b === btn); });
      if (targetView === 'calendar') render();
    });
  });

  var modeBtns = document.querySelectorAll('[data-mode-target]');
  modeBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      activeMode = btn.getAttribute('data-mode-target');
      modeBtns.forEach(function (b) {
        var active = b === btn;
        b.classList.toggle('active', active);
        b.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      document.querySelectorAll('.event-row[data-event-mode]').forEach(function (row) {
        row.hidden = activeMode !== 'all' && row.getAttribute('data-event-mode') !== activeMode;
      });
      render();
    });
  });

  document.addEventListener('click', function (e) {
    if (!popover || popover.contains(e.target) || grid.contains(e.target)) return;
    closePopover();
  });
}

// Event image upload: previews and remembers the selected image on this device.
(function(){
  const pathKey = 'ph-event-image:' + window.location.pathname;
  const upload = document.querySelector('[data-event-image-upload]');
  if (!upload) return;
  const input = upload.querySelector('[data-event-image-input]');
  const preview = upload.querySelector('[data-event-image-preview]');
  const frame = upload.querySelector('[data-event-image-frame]');
  const remove = upload.querySelector('[data-event-image-remove]');
  const reader = new FileReader();
  function show(src){ preview.src = src; frame.classList.add('has-image'); upload.classList.add('has-image'); }
  function clear(){ preview.removeAttribute('src'); frame.classList.remove('has-image'); upload.classList.remove('has-image'); localStorage.removeItem(pathKey); if(input) input.value=''; }
  input && input.addEventListener('change', function(){
    const file=this.files && this.files[0];
    if(!file || !file.type.startsWith('image/')) return;
    reader.onload=function(e){ const src=e.target.result; show(src); try{ localStorage.setItem(pathKey, src); }catch(err){} };
    reader.readAsDataURL(file);
  });
  remove && remove.addEventListener('click', clear);
  try{ const saved=localStorage.getItem(pathKey); if(saved) show(saved); }catch(err){}
})();
