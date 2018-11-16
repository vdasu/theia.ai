//
//  ViewController.swift
//  Theia
//
//  Created by Vishnu Dasu on 10/11/18.
//  Copyright © 2018 Vishnu Dasu. All rights reserved.
//

import UIKit
import AVFoundation

class ViewController: UIViewController {
    
    let synthesizer = AVSpeechSynthesizer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        let utterance = AVSpeechUtterance(string: "Tap anywhere to continue.")
        self.synthesizer.speak(utterance)
    }


}

