//
//  ViewController.swift
//  BouncerDisplay
//
//  Created by Sebastian Hunkeler on 28.06.17.
//  Copyright © 2017 Sbhklr. All rights reserved.
//

import UIKit
import Swifter
import AVKit
import AVFoundation
import Player

class ViewController: UIViewController, PlayerDelegate {
    func playerReady(_ player: Player) {
        
    }
    
    func playerPlaybackStateDidChange(_ player: Player) {
        
    }
    
    func playerBufferingStateDidChange(_ player: Player) {
        
    }
    
    func playerBufferTimeDidChange(_ bufferTime: Double) {
        
    }
    
    func player(_ player: Player, didFailWithError error: Error?) {
        
    }
    
    
    @IBOutlet weak var textView: UITextView!
    private var player:Player!
    private var server:HttpServer?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        UIApplication.shared.isIdleTimerDisabled = true
        
        do {
            let server = demoServer(Bundle.main.resourcePath!)
            try server.start(9080)
            self.server = server
            self.server?["/"] = { (request:HttpRequest) -> HttpResponse in
                let params = request.queryParams as [(String,String)]
                let display = params[0].1;
                DispatchQueue.main.async {
                    if(display == "debug") {
                        self.textView.backgroundColor = UIColor.purple
                    } else {
                        self.textView.backgroundColor = UIColor.clear
                        self.textView.text = display
                    }
                }
                return HttpResponse.ok(.html("Request: \(display)"))
            }
            
        } catch {
            print("Server start error: \(error)")
        }
        
        preparePlayer()
        
        if let videoUrl: URL = Bundle.main.url(forResource: "animation", withExtension: "mp4") {
            
            player.url = videoUrl
            player.playFromBeginning()
            view.bringSubview(toFront: textView)
        }
        
    }
    
    func preparePlayer() {
        self.player = Player()
        self.player.playerDelegate = self
        self.player.view.frame = self.view.bounds
        //self.player.fillMode = AVLayerVideoGravityResizeAspectFill
        self.player.playbackLoops = true
        
        self.addChildViewController(self.player)
        self.view.addSubview(self.player.view)
        self.player.didMove(toParentViewController: self)
    }

}

