import SwiftFoundation

var num = 0
var a = IndexSet()
for _ in 0..<500 {
    num += 2
    a.insert(num)
}

num = 0
var b = IndexSet()
for _ in 0..<500 {
    num += 2
    b.insert(num)
}

for _ in 0..<10000 {
    _ = a.union(b)
}