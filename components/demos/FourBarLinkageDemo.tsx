import React, { useState, useEffect } from 'react';

const FourBarMechanismDemo = () => {
  // Check if mechanism configuration is valid
  const checkGrashofCondition = (lengths) => {
    const sortedLengths = [lengths.linkA, lengths.linkB, lengths.linkC, lengths.linkD].sort((a, b) => a - b);
    const s = sortedLengths[0];
    const p = sortedLengths[1];
    const q = sortedLengths[2];
    const l = sortedLengths[3];
    
    // Grashof condition: s + l ≤ p + q
    return {
      isGrashof: s + l <= p + q,
      type: s + l < p + q ? "Grashof" : "Non-Grashof"
    };
  };

  const [inputAngle, setInputAngle] = useState(30);
  const [linkLengths, setLinkLengths] = useState({
    linkA: 40,  // Input link (ground to input)
    linkB: 120, // Coupler link
    linkC: 100, // Output link
    linkD: 150  // Ground link (fixed link)
  });
  const [mechanism, setMechanism] = useState({ 
    valid: true, 
    message: '',
    pointB: { x: 0, y: 0 },
    pointC: { x: 0, y: 0 },
    outputAngle: 0
  });
  const [isAnimating, setIsAnimating] = useState(false);
  
  // Canvas dimensions
  const width = 500;
  const height = 300;
  const margin = 60;
  const scale = 1.2;
  
  // Define fixed points
  const originX = margin;
  const originY = height - margin;
  const fixedPivotX = originX + linkLengths.linkD * scale;
  const fixedPivotY = originY;
  
  // Animation effect
  useEffect(() => {
    let animationId;
    
    if (isAnimating) {
      let lastTimestamp = 0;
      const step = (timestamp) => {
        if (!lastTimestamp) lastTimestamp = timestamp;
        const elapsed = timestamp - lastTimestamp;
        
        // Update angle at a rate of 60 degrees per second
        if (elapsed > 16) {  // Update every ~16ms (60fps)
          setInputAngle((prevAngle) => (prevAngle + 1) % 360);
          lastTimestamp = timestamp;
        }
        
        animationId = requestAnimationFrame(step);
      };
      
      animationId = requestAnimationFrame(step);
    }
    
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
    };
  }, [isAnimating]);
  
  // Calculate positions
  const calculateMechanism = () => {
    // Convert input angle to radians
    const theta1 = (inputAngle * Math.PI) / 180;
    
    // Calculate position of point B (end of input link)
    const Bx = originX + linkLengths.linkA * scale * Math.cos(theta1);
    const By = originY - linkLengths.linkA * scale * Math.sin(theta1);
    
    // Now we need to find point C
    // It must be at distance linkB from B and distance linkC from the fixed pivot D
    // This is an intersection of two circles problem
    
    const a = linkLengths.linkB * scale;
    const b = linkLengths.linkC * scale;
    const c = Math.sqrt((fixedPivotX - Bx) ** 2 + (fixedPivotY - By) ** 2);
    
    // Check if the mechanism is valid (triangle inequality)
    if (c > a + b || c < Math.abs(a - b)) {
      return {
        valid: false,
        message: "Mechanism cannot be assembled in this configuration",
        pointB: { x: Bx, y: By },
        pointC: { x: fixedPivotX, y: fixedPivotY }
      };
    }
    
    // Calculate position of point C using the law of cosines
    const alpha = Math.acos((a*a + c*c - b*b) / (2 * a * c));
    
    // Find the angle between the x-axis and the line from B to D
    const beta = Math.atan2(fixedPivotY - By, fixedPivotX - Bx);
    
    // There are two possible positions for C, we'll choose the one above the BD line
    const Cx = Bx + a * Math.cos(beta + alpha);
    const Cy = By + a * Math.sin(beta + alpha);
    
    // Calculate the output angle (angle of linkC with horizontal)
    const outputAngle = Math.atan2(fixedPivotY - Cy, fixedPivotX - Cx) * 180 / Math.PI;
    
    return {
      valid: true,
      message: "",
      pointB: { x: Bx, y: By },
      pointC: { x: Cx, y: Cy },
      outputAngle: outputAngle
    };
  };
  
  // Update mechanism position when input changes
  useEffect(() => {
    const result = calculateMechanism();
    setMechanism(result);
  }, [inputAngle, linkLengths]);
  
  // Check Grashof condition
  const grashofStatus = checkGrashofCondition(linkLengths);
  
  return (
    <div className="tw-flex tw-flex-col tw-items-center tw-p-4 tw-bg-white tw-rounded-lg tw-shadow">
      <h3 className="tw-text-xl tw-font-bold tw-mb-4">Four-Bar Linkage</h3>
      
      <div className="tw-mb-4 tw-w-full">
        <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="tw-border tw-border-gray-300 tw-bg-gray-50">
          {/* Fixed pivots */}
          <circle cx={originX} cy={originY} r={5} fill="#1F2937" />
          <circle cx={fixedPivotX} cy={fixedPivotY} r={5} fill="#1F2937" />
          
          {/* Ground link */}
          <line 
            x1={originX} 
            y1={originY} 
            x2={fixedPivotX} 
            y2={fixedPivotY} 
            stroke="#9CA3AF" 
            strokeWidth={3} 
            strokeDasharray="8,4"
          />
          
          {mechanism.valid ? (
            <>
              {/* Input link */}
              <line 
                x1={originX} 
                y1={originY} 
                x2={mechanism.pointB.x} 
                y2={mechanism.pointB.y} 
                stroke="#EF4444" 
                strokeWidth={4} 
              />
              
              {/* Coupler link */}
              <line 
                x1={mechanism.pointB.x} 
                y1={mechanism.pointB.y} 
                x2={mechanism.pointC.x} 
                y2={mechanism.pointC.y} 
                stroke="#3B82F6" 
                strokeWidth={3} 
              />
              
              {/* Output link */}
              <line 
                x1={mechanism.pointC.x} 
                y1={mechanism.pointC.y} 
                x2={fixedPivotX} 
                y2={fixedPivotY} 
                stroke="#10B981" 
                strokeWidth={3} 
              />
              
              {/* Joints */}
              <circle cx={mechanism.pointB.x} cy={mechanism.pointB.y} r={4} fill="#6366F1" />
              <circle cx={mechanism.pointC.x} cy={mechanism.pointC.y} r={4} fill="#6366F1" />
              
              {/* Labels */}
              <text x={originX - 20} y={originY - 15} className="tw-text-sm" fill="#1F2937">A</text>
              <text x={mechanism.pointB.x + 10} y={mechanism.pointB.y} className="tw-text-sm" fill="#1F2937">B</text>
              <text x={mechanism.pointC.x + 10} y={mechanism.pointC.y} className="tw-text-sm" fill="#1F2937">C</text>
              <text x={fixedPivotX + 10} y={fixedPivotY - 15} className="tw-text-sm" fill="#1F2937">D</text>
              
              {/* Measurements */}
              <text x={originX + linkLengths.linkA * scale/2 - 20} y={originY - 20} className="tw-text-xs" fill="#EF4444">
                Link AB: {linkLengths.linkA}mm
              </text>
              <text x={(mechanism.pointB.x + mechanism.pointC.x)/2 - 20} y={(mechanism.pointB.y + mechanism.pointC.y)/2 - 10} className="tw-text-xs" fill="#3B82F6">
                Link BC: {linkLengths.linkB}mm
              </text>
              <text x={(mechanism.pointC.x + fixedPivotX)/2 - 20} y={(mechanism.pointC.y + fixedPivotY)/2 + 20} className="tw-text-xs" fill="#10B981">
                Link CD: {linkLengths.linkC}mm
              </text>
            </>
          ) : (
            <text x={width/2 - 100} y={height/2} className="tw-text-base" fill="#EF4444">{mechanism.message}</text>
          )}
        </svg>
      </div>
      
      <div className="tw-w-full tw-flex tw-flex-col md:tw-flex-row md:tw-justify-between tw-gap-4">
        <div className="tw-flex tw-flex-col tw-gap-2 tw-w-full md:tw-w-1/2">
          <label className="tw-font-medium tw-text-gray-700">Input Angle: {inputAngle}°</label>
          <input 
            type="range" 
            min="0" 
            max="359" 
            value={inputAngle} 
            onChange={(e) => setInputAngle(parseInt(e.target.value))}
            disabled={isAnimating}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2 tw-w-full md:tw-w-1/2">
          <label className="tw-font-medium tw-text-gray-700">
            Output Angle: {mechanism.valid ? Math.round(mechanism.outputAngle) : "N/A"}°
          </label>
          <div className="tw-w-full tw-h-8 tw-bg-gray-200 tw-rounded">
            {mechanism.valid && (
              <div 
                className="tw-h-full tw-bg-blue-500 tw-rounded" 
                style={{ width: `${Math.abs(mechanism.outputAngle) / 3.6}%` }}
              ></div>
            )}
          </div>
        </div>
      </div>
      
      <div className="tw-w-full tw-grid tw-grid-cols-2 md:tw-grid-cols-4 tw-gap-4 tw-mt-4">
        <div className="tw-flex tw-flex-col tw-gap-2">
          <label className="tw-font-medium tw-text-gray-700">Input Link (AB): {linkLengths.linkA}mm</label>
          <input 
            type="range" 
            min="20" 
            max="80" 
            value={linkLengths.linkA} 
            onChange={(e) => setLinkLengths({...linkLengths, linkA: parseInt(e.target.value)})}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2">
          <label className="tw-font-medium tw-text-gray-700">Coupler (BC): {linkLengths.linkB}mm</label>
          <input 
            type="range" 
            min="60" 
            max="180" 
            value={linkLengths.linkB} 
            onChange={(e) => setLinkLengths({...linkLengths, linkB: parseInt(e.target.value)})}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2">
          <label className="tw-font-medium tw-text-gray-700">Output Link (CD): {linkLengths.linkC}mm</label>
          <input 
            type="range" 
            min="60" 
            max="150" 
            value={linkLengths.linkC} 
            onChange={(e) => setLinkLengths({...linkLengths, linkC: parseInt(e.target.value)})}
            className="tw-w-full"
          />
        </div>
        
        <div className="tw-flex tw-flex-col tw-gap-2">
          <label className="tw-font-medium tw-text-gray-700">Ground Link (AD): {linkLengths.linkD}mm</label>
          <input 
            type="range" 
            min="100" 
            max="200" 
            value={linkLengths.linkD} 
            onChange={(e) => setLinkLengths({...linkLengths, linkD: parseInt(e.target.value)})}
            className="tw-w-full"
          />
        </div>
      </div>
      
      <div className="tw-mt-4 tw-flex tw-gap-4">
        <button 
          onClick={() => setIsAnimating(!isAnimating)}
          className="tw-px-4 tw-py-2 tw-bg-blue-600 tw-text-white tw-rounded hover:tw-bg-blue-700 tw-transition"
        >
          {isAnimating ? 'Pause' : 'Animate'}
        </button>
        
        <button
          onClick={() => {
            setLinkLengths({
              linkA: 40,
              linkB: 120,
              linkC: 100,
              linkD: 150
            });
            setInputAngle(30);
            setIsAnimating(false);
          }}
          className="tw-px-4 tw-py-2 tw-bg-gray-600 tw-text-white tw-rounded hover:tw-bg-gray-700 tw-transition"
        >
          Reset
        </button>
      </div>
      
      <div className="tw-mt-4 tw-text-gray-700">
        <div className="tw-p-3 tw-bg-gray-100 tw-rounded tw-mb-3">
          <p className="tw-text-sm tw-font-semibold">
            Grashof Condition: {grashofStatus.isGrashof ? (
              <span className="tw-text-green-600">{grashofStatus.type} (Full Rotation Possible)</span>
            ) : (
              <span className="tw-text-amber-600">{grashofStatus.type} (Limited Motion)</span>
            )}
          </p>
        </div>
        
        <p className="tw-text-sm">
          <strong>Input Link Angle:</strong> {inputAngle}° from horizontal
        </p>
        {mechanism.valid && (
          <p className="tw-text-sm">
            <strong>Output Link Angle:</strong> {Math.round(mechanism.outputAngle)}° from horizontal
          </p>
        )}
        {!mechanism.valid && (
          <p className="tw-text-sm tw-mt-2 tw-text-red-500 tw-font-medium">
            {mechanism.message}. Try adjusting the link lengths to create a valid mechanism.
          </p>
        )}
      </div>
    </div>
  );
};

export default FourBarMechanismDemo;
