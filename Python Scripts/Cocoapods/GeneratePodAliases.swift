#!/usr/bin/env swift
//
//  main.swift
//  GeneratePodEnvVars
//
//  Created by Steven Barnegren on 03/05/2017.
//  Copyright © 2017 SteveBarnegren. All rights reserved.
//

import Foundation

let ROOT_POD_SEARCH_PATH = NSHomeDirectory() + "/Documents"

// MARK: - String Utils

public extension String {
    
    var length: Int {
        return count
    }
    
    var pathExtension: String {
        return (self as NSString).pathExtension
    }
    
    func deletingPathExtension() -> String {
        return (self as NSString).deletingPathExtension
    }
    
    func contains(subString: String) -> Bool{
        return self.range(of: subString) != nil
    }
    
}

// MARK: - Dictionaty extensions

extension Dictionary where Key == String, Value == [String] {
    
    mutating func addPod(withName name: String, path: String) {
        
        if var existingPaths = self[name] {
            
            if existingPaths.contains(path) {
                return
            }
            
            existingPaths.append(path)
            self[name] = existingPaths
        }
        else{
            self[name] = [path]
        }
    }
    
    mutating func addItemsFromOther(_ other: Dictionary) {
        
        for podName in other.keys {
            for path in other[podName]! {
                self.addPod(withName: podName, path: path)
            }
        }
    }
}

// MARK: - Notifications

class NotifDelegate: NSObject, NSUserNotificationCenterDelegate {
    func userNotificationCenter(_ center: NSUserNotificationCenter, shouldPresent notification: NSUserNotification) -> Bool {
        return true
    }
}

func postNotification(withTitle title: String, message: String) {
    
    var error: NSDictionary?
    NSAppleScript(source: "display notification \"\(message)\" with title \"\(title)\"")?.executeAndReturnError(&error)
    if error != nil {
        print("Error: \(error!)")
    }
}

// MARK: - Traverse file system

func podsInPath(_ path: String, ignoreDirectories: Bool = false) -> Dictionary<String, [String]> {
    
    var pods = [ String : [String] ]()
    
    let itemName = path.components(separatedBy: "/").last!
    
    // Exclude hidden files and folders
    if itemName.count > 0, itemName.first == "." {
        return pods
    }
    
    // Check if the directory actually exists
    var isDirectory: ObjCBool = false
    let exists = fileManager.fileExists(atPath: path, isDirectory: &isDirectory)
    
    guard exists else{
        return pods
    }
    
    // Find if is a package (a folder with a file extension, we won't search these)
    if isDirectory.boolValue && itemName.contains(".") {
        return pods
    }
    
    // If it's a directory
    if isDirectory.boolValue {
        
        if ignoreDirectories {
            return pods
        }
        
        guard let contents = try? fileManager.contentsOfDirectory(atPath: path) else {
            return pods
        }
        
        var ignoreDirectory = false
        contents.forEach{
            if $0.contains("xcodeproj") ||
                $0.contains("xcworkspace") ||
                $0.contains("node_modules") ||
                $0.contains("AFImageHelper") {
                
                ignoreDirectory = true
            }
        }
        
        contents.map{ "\(path)" + "/" + $0 }
            .compactMap{ podsInPath($0, ignoreDirectories: ignoreDirectory) }
            .forEach{
                pods.addItemsFromOther($0)
        }
        
        return pods
    }
    else{
        
        let nameWithExtension = path.components(separatedBy: "/").last!
        
        let fileName = nameWithExtension.deletingPathExtension()
        let fileExt = nameWithExtension.pathExtension
        
        if fileExt == "podspec" {
            print("Found pod \(fileName) at: \(path)")
            
            let folderPath = path.replacingOccurrences(of: nameWithExtension, with: "", options: .literal, range: nil)
            pods.addPod(withName: fileName, path: folderPath)
        }
        
        return pods
    }
    
}

// MARK: - Main

let fileManager = FileManager.default

let pods = podsInPath(ROOT_POD_SEARCH_PATH)
var multiplePathPodNames = [String]()
var successfullyAddedPodNames = [String]()
var fileString = ""

for podName in pods.keys {
    
    let paths = pods[podName]!
    
    if paths.count == 1 {
        if fileString.length > 0 {
            fileString = fileString + "\n"
        }
        fileString = fileString + "export \(podName)=\"\(paths.first!)\""
        successfullyAddedPodNames.append(podName)
    }
    else{
        multiplePathPodNames.append(podName);
    }
}

// Print errors for pods with multiple paths
if multiplePathPodNames.count > 0 {
    
    print("ERROR - Some pods were found at multiple paths:")
    
    for podName in multiplePathPodNames {
        
        // Print error
        let paths = pods[podName]!
        print("\(podName):")
        paths.forEach{
            print("- \($0)")
        }
        
        // Append errors to file
        fileString.append("\n")
        fileString.append("\n# ERROR: Multiple paths for pod '\(podName)'")
        paths.forEach{
            fileString.append("\n# \($0)")
        }
    }
}

// Add update time to file
let date = Date()
let dateFormatter = DateFormatter()
dateFormatter.dateFormat = "dd-MM-yyyy HH:mm"
let dateString = dateFormatter.string(from: date)
fileString.append("\n\n# Last Updated: \(dateString)")

// Create directory

let directoryPath = NSHomeDirectory() + "/.podAliases"

if fileManager.fileExists(atPath: directoryPath) == false {
    
    do{
        try fileManager.createDirectory(atPath: directoryPath, withIntermediateDirectories: false, attributes: nil)
    }
    catch let error as NSError {
        print("Error creating directory: \(error)")
        exit(1)
    }
}

// Write the file
do{
    try fileString.write(toFile: directoryPath + "/PodAliases", atomically: false, encoding: .utf8)
}
catch let error as NSError {
    print("Error writing file: \(error)")
    exit(1)
}

// Print Success
print("\nSuccessfully added environment variables for pods:\n")
successfullyAddedPodNames.forEach{
    print("\($0)")
}

