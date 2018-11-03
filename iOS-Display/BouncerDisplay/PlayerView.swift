import AVFoundation
import UIKit

class PlayerView: UIView {
    
    override class var layerClass: AnyClass {
        return AVPlayerLayer.self
    }
    
    
    var player:AVPlayer? {
        set {
            if let layer = layer as? AVPlayerLayer {
                layer.player = player
            }
        }
        get {
            if let layer = layer as? AVPlayerLayer {
                return layer.player
            } else {
                return nil
            }
        }
    }
}
