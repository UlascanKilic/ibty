function RoomEntity(id, skin, posX, posY){
    RoomContent.call(this, id, skin, posX, posY, "entity");
    this.skin=skin;
    this.offsetX = json.entities[this.skin].offsetX;
    this.offsetY = json.entities[this.skin].offsetY;
    this.updateTextureSourceElement();

    this.update = function(deltaTime){
        
    };
    this.onclick = function(){
        console.log("entity", this.id);
        socket.emit("click", {"id":this.id, "type":"room_object"});
    };
}
