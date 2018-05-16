function NPC(id, skin, posX, posY, nick) {
    this.totalAnimation = 3;
    this.animState = 0;
    this.moveState = false;
    this.direction = "S";
    this.skin = skin;
    this.offsetX = json.characters[this.skin].offsetX;
    this.offsetY = json.characters[this.skin].offsetY;
    this.nick = nick;
  
    Character.call(this, id, skin , posX, posY, nick);

}
  
  