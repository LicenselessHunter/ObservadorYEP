let tableComandsProduct = document.getElementById('Table-Comands-Product'); //Se recoge el div con los controles de producto.
let AddButtonMarketplace = document.getElementById('AddButtonMarketplace');

let GROUPSALE_COMANDS = document.getElementById('GROUPSALE_COMANDS'); //Se recoge el div con los controles de producto.
let InviteButton = document.getElementById('invite-button') //Se recoge el botón de invitación.

let add_sales_button = document.getElementById('add_sales_button');

let StatisticsTimeFilters = document.getElementById('Statistics-Time-Filters');
let FinalizedSalesFilters = document.getElementById('Finalized-sales-Filters');

if (window.location.pathname.endsWith('tables/')) 
{ //Si es que el usuario esta en la ventana de productos el div con los controles de tabla se hará visible.

	tableComandsProduct.style.visibility = "visible";

}

else if (window.location.pathname.endsWith('/marketplaces/'))
{

	AddButtonMarketplace.style.visibility = "visible";

}


else if (window.location.href.indexOf("SalesGroup_detail") > -1)
{
	GROUPSALE_COMMANDS.style.visibility = "visible";

	var modalPopupComparison = new bootstrap.Modal(document.getElementById("comparison_import_errorModal"), {backdrop: 'static', keyboard: false}); /*Instancia de Modal, los párarmetos que se le pasan en las {} son para evitar que se pueda cerrar el modal si se presiona fuera de el.*/
	modalPopupComparison.show(); /*Esto es para mostrar el modal de errores en la página de products en caso de error de importación*/
}

else if (window.location.pathname.endsWith('Accounts/'))
{

	InviteButton.style.visibility = "visible";

}


else if (window.location.pathname.endsWith('sales_on_standby'))
{

	add_sales_button.style.visibility = "visible";

	var modalPopupSaleImport = new bootstrap.Modal(document.getElementById("import_errorModal"), {backdrop: 'static', keyboard: false});/*Instancia de Modal, los párarmetos que se le pasan en las {} son para evitar que se pueda cerrar el modal si se presiona fuera de el.*/
	modalPopupSaleImport.show(); 


}

else if (window.location.pathname.endsWith('dashboard/'))
{

	StatisticsTimeFilters.style.visibility = "visible";

}

else if (window.location.pathname.endsWith('Sales/'))
{

	FinalizedSalesFilters.style.visibility = "visible";
	
}