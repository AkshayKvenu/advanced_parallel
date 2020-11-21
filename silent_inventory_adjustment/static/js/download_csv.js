odoo.define('silent_inventory_adjustment.ActionManager', function (require) {
"use strict";
    var ActionManager = require('web.ActionManager');
    var crash_manager = require('web.crash_manager');
    var framework = require('web.framework');
    var core = require('web.core');
    var _lt = core._lt;
    var trigger_csv_download = function(session, response, c, action, options) {
        var def = $.Deferred();
        session.get_file({
            url: '/report/csv',
            data: {data: JSON.stringify(response)},
            complete: framework.unblockUI,
            error: c.rpc_error.bind(c),
            success: function(){
                if (action && options && !action.dialog) {
                    options.on_close();
                }
//                self.dialog_stop();
                def.resolve();
            },
        });
        return def;
    };

    // Messages that might be shown to the user dependening on the state of wkhtmltopdf
    var link = '<br><br><a href="http://wkhtmltopdf.org/" target="_blank">wkhtmltopdf.org</a>';
    var WKHTMLTOPDF_MESSAGES = {
        broken: _lt('Your installation of Wkhtmltopdf seems to be broken. The report will be shown ' +
                    'in html.') + link,
        install: _lt('Unable to find Wkhtmltopdf on this system. The report will be shown in ' +
                     'html.') + link,
        upgrade: _lt('You should upgrade your version of Wkhtmltopdf to at least 0.12.0 in order to ' +
                     'get a correct display of headers and footers as well as support for ' +
                     'table-breaking between pages.') + link,
        workers: _lt('You need to start Odoo with at least two workers to print a pdf version of ' +
                     'the reports.'),
    };

    ActionManager.include({
        _executeReportAction: function (action, options) {
        var self = this;

        if (action.report_type === 'qweb-html') {
            return this._executeReportClientAction(action, options);
        } else if (action.report_type === 'qweb-pdf') {
            // check the state of wkhtmltopdf before proceeding
            return this.call('report', 'checkWkhtmltopdf').then(function (state) {
                // display a notification according to wkhtmltopdf's state
                if (state in WKHTMLTOPDF_MESSAGES) {
                    self.do_notify(_t('Report'), WKHTMLTOPDF_MESSAGES[state], true);
                }

                if (state === 'upgrade' || state === 'ok') {
                    // trigger the download of the PDF report
                    return self._triggerDownload(action, options, 'pdf');
                } else {
                    // open the report in the client action if generating the PDF is not possible
                    return self._executeReportClientAction(action, options);
                }
            });
        } else if (action.report_type === 'qweb-text') {
            return self._triggerDownload(action, options, 'text');
        } else if (action.report_type === 'qweb-csv') {
//            return self._triggerDownload(action, options, 'csv');
                console.log(self.getSession());
                var response = new Array();
            	response[0] = action.data
            	var c = crash_manager;
            	return trigger_csv_download(self.getSession(), response, c, action, options);
        } else {
            console.error("The ActionManager can't handle reports of type " +
                action.report_type, action);
            return $.Deferred().reject();
        }
    },
    });


});
