import Vec2 from "./vec2";
import d3 from "d3";
export default Arc;

function Arc(x, y, startAngle, endAngle, radius) {
    this.center = new Vec2(x, y);
    this.startAngle = startAngle;
    this.endAngle = endAngle;
    this.radius = radius;
}