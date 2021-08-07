const Yoga = require('yoga-layout-wasm');

function test() {
    const Node = Yoga.Node
    const root = Node.create();
    root.setWidth(500);
    root.setHeight(300);
    root.setJustifyContent(Yoga.JUSTIFY_CENTER);

    const node1 = Node.create();
    node1.setWidth(100);
    node1.setHeight(100);

    const node2 = Node.create();
    node2.setWidth(100);
    node2.setHeight(100);

    root.insertChild(node1, 0);
    root.insertChild(node2, 1);

    root.calculateLayout(500, 300, Yoga.DIRECTION_LTR);
    console.log(root.getComputedLayout());
    // {left: 0, top: 0, width: 500, height: 300}
    console.log(node1.getComputedLayout());
    // {left: 150, top: 0, width: 100, height: 100}
    console.log(node2.getComputedLayout());
    // {left: 250, top: 0, width: 100, height: 100}
}

const wasmFilePath = 'node_modules/yoga-layout-wasm/dist/yoga.wasm'

Yoga.init(wasmFilePath).then(test)