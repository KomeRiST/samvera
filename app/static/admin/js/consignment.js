$(function(){
    // on page load...
    function Calculate() {
        for (let i = 0; i < id_cost.length; i++) {
            field_total_not_nds[i].value = id_cost[i].value * id_kolvo[i].value;
            field_total_nds[i].value = ((id_nds[i].value * id_cost[i].value / 100) * id_kolvo[i].value) + (id_kolvo[i].value * id_cost[i].value);
            field_nds_summ[i].value = (id_nds[i].value * id_cost[i].value / 100) * id_kolvo[i].value;
        }
    }
    function Init() {
        id_kolvo = document.querySelectorAll("input[name*='-kolvo']:not([name*='__prefix__'])");
        id_cost = document.querySelectorAll("input[name*='-cost']:not([name*='__prefix__'])");
        id_nds = document.querySelectorAll("input[name$='-nds']:not([name*='__prefix__'])");
        // console.log(id_kolvo);
        // console.log(id_cost);
        // console.log(id_nds);
        id_kolvo.forEach(item => {
            item.oninput = Calculate;
        });
        id_cost.forEach(item => {
            item.oninput = Calculate;
        });
        id_nds.forEach(item => {
            item.oninput = Calculate;
        });
        field_nds_summ = document.querySelectorAll('[id*="-nds_summ"]:not([name*="__prefix__"])');
        field_total_not_nds = document.querySelectorAll('[id*="-total_not_nds"]:not([name*="__prefix__"])');
        field_total_nds= document.querySelectorAll('[id*="-total_nds"]:not([name*="__prefix__"])');
    };
    Init();
    document.getElementById("in_consignments-group").addEventListener("DOMSubtreeModified", Init);
});