//
//  InferenceController.swift
//  Theia
//
//  Created by Vishnu Dasu on 10/11/18.
//  Copyright © 2018 Vishnu Dasu. All rights reserved.
//

import UIKit
import AVFoundation

class InferenceController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    let synthesizer = AVSpeechSynthesizer()
    let uploadURL = URL(string: "http://127.0.0.1:8000/")
    var actionToPerform = ""
    let imagePicker = UIImagePickerController()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        imagePicker.delegate = self
        imagePicker.allowsEditing = false
        imagePicker.sourceType = .photoLibrary
        chooseImageOutlet.backgroundColor = .clear
        chooseImageOutlet.layer.cornerRadius = 5
        chooseImageOutlet.layer.borderWidth = 1
        chooseImageOutlet.layer.borderColor = UIColor.white.cgColor
    }
    
    @IBOutlet weak var imageOutlet: UIImageView!
    @IBOutlet weak var labelOutlet: UILabel!
    @IBOutlet weak var chooseImageOutlet: UIButton!
    
    @IBAction func pickImageAction(_ sender: Any) {
        present(imagePicker, animated: true, completion: nil)
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
        if let pickedImage = info[UIImagePickerController.InfoKey.originalImage] as? UIImage {
//            self.imageOutlet.contentMode = .scaleAspectFit
            self.imageOutlet.image = pickedImage
        }
        sendImageToServer()
        self.labelOutlet.text = self.actionToPerform
        dismiss(animated: true, completion: nil)
    }
    
    func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
        dismiss(animated: true, completion: nil)
    }
    
    func sendImageToServer() {
        
        let image = imageOutlet.image!
        let imageData = image.jpegData(compressionQuality: 1.0)
        var postRequest = URLRequest.init(url: uploadURL!)
        postRequest.httpMethod = "POST"
        postRequest.httpBody = imageData
        var responseString = ""
        
        let uploadSession = URLSession.shared
        let executePostRequest = uploadSession.dataTask(with: postRequest as URLRequest) { (data, response, error) -> Void in
            if let response = response as? HTTPURLResponse
            {
                print(response.statusCode)
            }
            if let data = data
            {
                let json = String(data: data, encoding: String.Encoding.utf8)
                responseString = String(describing: json!)
                let utterance = AVSpeechUtterance(string: responseString)
                print(responseString)
                DispatchQueue.main.async {
                    self.labelOutlet.text = responseString
                }
                self.synthesizer.speak(utterance)
            }
        }
        executePostRequest.resume()
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
