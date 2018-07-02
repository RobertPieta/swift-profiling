import SwiftFoundation

var num = 0
let a = NSMutableIndexSet()
for _ in 0..<2000 {
    num += 2
    a.add(num)
}

for _ in 0..<10000 {
	let b = a.mutableCopy() as! NSMutableIndexSet
	b.add(20002)
}