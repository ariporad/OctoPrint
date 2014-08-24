function FilamentsViewModel() {
    var self = this;

    // initialize list helper
    self.listHelper = new ItemListHelper(
        "filaments",
        {
            "name": function(a, b) {
                // sorts ascending
                if (a["name"].toLocaleLowerCase() < b["name"].toLocaleLowerCase()) return -1;
                if (a["name"].toLocaleLowerCase() > b["name"].toLocaleLowerCase()) return 1;
                return 0;
            }
        },
        {},
        "name",
        [],
        [],
        CONFIG_filamentSPERPAGE
    );

    self.emptyfilament = {name: "", admin: false, active: false};

    self.currentfilament = ko.observable(self.emptyfilament);

    self.editorfilamentname = ko.observable(undefined);
    self.editorPassword = ko.observable(undefined);
    self.editorRepeatedPassword = ko.observable(undefined);
    self.editorApikey = ko.observable(undefined);
    self.editorAdmin = ko.observable(undefined);
    self.editorActive = ko.observable(undefined);

    self.currentfilament.subscribe(function(newValue) {
        if (newValue === undefined) {
            self.editorfilamentname(undefined);
            self.editorAdmin(undefined);
            self.editorActive(undefined);
            self.editorApikey(undefined);
        } else {
            self.editorfilamentname(newValue.name);
            self.editorAdmin(newValue.admin);
            self.editorActive(newValue.active);
            self.editorApikey(newValue.apikey);
        }
        self.editorPassword(undefined);
        self.editorRepeatedPassword(undefined);
    });

    self.editorPasswordMismatch = ko.computed(function() {
        return self.editorPassword() != self.editorRepeatedPassword();
    });

    self.requestData = function() {
        $.ajax({
            url: API_BASEURL + "filaments",
            type: "GET",
            dataType: "json",
            success: self.fromResponse
        });
    }

    self.fromResponse = function(response) {
        self.listHelper.updateItems(response.filaments);
    }

    self.showAddFilamentDialog = function() {
        $("#settings-filamentsDialogAddFilament").modal("show");
    }

    self.showEditFilamentDialog = function(filament) {
        self.currentfilament(filament);
        $("#settings-filamentsDialogEditfilament").modal("show");
    }

    self.addFilament = function(filament, callback) {
        if (filament === undefined) return;

        $.ajax({
            url: API_BASEURL + "filaments",
            type: "POST",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(filament),
            success: function(response) {
                self.fromResponse(response);
                callback();
            }
        });
    }

    self.removefilament = function(filament, callback) {
        if (filament === undefined) return;

        $.ajax({
            url: API_BASEURL + "filaments/" + filament.name,
            type: "DELETE",
            success: function(response) {
                self.fromResponse(response);
                callback();
            }
        });
    }

    self.updatefilament = function(filament, callback) {
        if (filament === undefined) return;

        $.ajax({
            url: API_BASEURL + "filaments/" + filament.name,
            type: "PUT",
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(filament),
            success: function(response) {
                self.fromResponse(response);
                callback();
            }
        });
    }
}
