(function () {
    function crearCustomSelect(select) {
        var wrap = document.createElement('div');
        wrap.className = 'custom-select-wrap';

        var trigger = document.createElement('button');
        trigger.type = 'button';
        trigger.className = 'custom-select-trigger';
        trigger.setAttribute('aria-haspopup', 'listbox');

        var valor = document.createElement('span');
        valor.className = 'custom-select-value';

        var flecha = document.createElement('span');
        flecha.className = 'custom-select-arrow';

        trigger.appendChild(valor);
        trigger.appendChild(flecha);

        var lista = document.createElement('ul');
        lista.className = 'custom-select-list';
        lista.setAttribute('role', 'listbox');

        Array.prototype.forEach.call(select.options, function (opcion) {
            var item = document.createElement('li');
            item.setAttribute('role', 'option');
            item.dataset.value = opcion.value;
            item.textContent = opcion.textContent;
            lista.appendChild(item);
        });

        select.classList.add('custom-select-hidden');
        select.parentNode.insertBefore(wrap, select);
        wrap.appendChild(trigger);
        wrap.appendChild(lista);
        wrap.appendChild(select);

        function actualizarValor() {
            valor.textContent = select.options[select.selectedIndex]
                ? select.options[select.selectedIndex].textContent
                : '';
            Array.prototype.forEach.call(lista.children, function (li) {
                li.classList.toggle('selected', li.dataset.value === select.value);
            });
        }

        function cerrar() {
            lista.classList.remove('open');
            wrap.classList.remove('open');
            document.removeEventListener('click', clicFuera, true);
        }

        function clicFuera(e) {
            if (!wrap.contains(e.target)) {
                cerrar();
            }
        }

        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            var abierto = lista.classList.contains('open');
            cerrar();
            if (!abierto) {
                lista.classList.add('open');
                wrap.classList.add('open');

                var rect = trigger.getBoundingClientRect();
                var espacioDebajo = window.innerHeight - rect.bottom;
                if (espacioDebajo < 200) {
                    trigger.scrollIntoView({ block: 'center' });
                }

                var maxAlto = Math.max(80, window.innerHeight - trigger.getBoundingClientRect().bottom - 16);
                lista.style.maxHeight = maxAlto + 'px';
                document.addEventListener('click', clicFuera, true);
            }
        });

        Array.prototype.forEach.call(lista.children, function (li) {
            li.addEventListener('click', function (e) {
                e.stopPropagation();
                select.value = li.dataset.value;
                select.dispatchEvent(new Event('change', { bubbles: true }));
                actualizarValor();
                cerrar();
            });
        });

        actualizarValor();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('select.custom-select').forEach(crearCustomSelect);
    });
})();