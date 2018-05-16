function PutEntities(room) {
    var entities;
    var entityJson = function () {
        $.ajaxSetup({
            async: false
        });
        var jsonTemp = null;
        $.getJSON("entity.json", function (data) {
            jsonTemp = data;
        });
        return jsonTemp;
    }();

    this.put = function () {
        for (k = 0; k < entityJson.length; k++) {
         //   console.log(entityJson[k].id, entityJson[k].name, entityJson[k].x, entityJson[k].y);
         console.log(entityJson[k].name);
            entities = new RoomEntity(entityJson[k].id, entityJson[k].name,entityJson[k].x, entityJson[k].y);
            
            room.yerlestir(entities);
        }
    };
}