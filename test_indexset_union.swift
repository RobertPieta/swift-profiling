import SwiftFoundation

for _ in 0..<100 {
    var num = 0
    var a = IndexSet()
    for _ in 0...1000 {
        num += Int.random(in: 1..<10)
        a.insert(num)
    }

    num = 0
    var b = IndexSet()
    for _ in 0..<50 {
        num += Int.random(in: 1..<10)
        b.insert(num)
    }

    _ = a.union(b)
}